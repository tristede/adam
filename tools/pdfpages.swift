// Convertit un PDF en une image par page, sans navigateur.
//
//   swiftc -O -o /tmp/pdfpages tools/pdfpages.swift
//   /tmp/pdfpages docs/mon.pdf images mon-prefixe
//
// La voie normale reste le bouton « PDF » de l'admin (pdf.js, sortie WebP).
// Ce script sert quand la conversion doit se faire en local : il reprend les
// memes reglages — echelle min(2, 1600/largeur), qualite 0.82 — et sort en
// WebP si la machine sait l'encoder, en JPEG sinon.

import Foundation
import PDFKit
import ImageIO
import CoreGraphics
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 4 else {
    FileHandle.standardError.write("usage: pdfpages <in.pdf> <outdir> <prefix>\n".data(using:.utf8)!)
    exit(2)
}
let inURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2])
let prefix = args[3]

guard let doc = PDFDocument(url: inURL) else {
    FileHandle.standardError.write("cannot open pdf\n".data(using:.utf8)!); exit(1)
}

// Which encoders does this machine actually have?
let ids = CGImageDestinationCopyTypeIdentifiers() as! [String]
let webpUTI = "org.webmproject.webp"
let useWebP = ids.contains(webpUTI)
let uti = useWebP ? webpUTI : (UTType.jpeg.identifier)
let ext = useWebP ? "webp" : "jpg"
FileHandle.standardError.write("encoder: \(uti)\n".data(using:.utf8)!)

for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let bounds = page.bounds(for: .mediaBox)
    // same rule as the admin's pdf.js path: cap at 2x, target 1600px wide
    let scale = min(2.0, 1600.0 / bounds.width)
    let w = Int((bounds.width * scale).rounded())
    let h = Int((bounds.height * scale).rounded())

    guard let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8,
                              bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(),
                              bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { continue }
    ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: w, height: h))
    // Deborder d'1 px sur chaque bord. Sans ca, un arrondi d'un demi-pixel
    // laisse le fond blanc affleurer sur une rangee — visible comme un filet
    // gris en haut d'une page a fond sombre.
    let bleed: CGFloat = 1
    ctx.translateBy(x: -bleed, y: -bleed)
    ctx.scaleBy(x: (CGFloat(w) + 2 * bleed) / CGFloat(w),
                y: (CGFloat(h) + 2 * bleed) / CGFloat(h))
    ctx.scaleBy(x: scale, y: scale)
    ctx.translateBy(x: -bounds.origin.x, y: -bounds.origin.y)
    page.draw(with: .mediaBox, to: ctx)

    guard let img = ctx.makeImage() else { continue }
    let out = outDir.appendingPathComponent("\(prefix)-\(i).\(ext)")
    guard let dest = CGImageDestinationCreateWithURL(out as CFURL, uti as CFString, 1, nil) else { continue }
    CGImageDestinationAddImage(dest, img, [kCGImageDestinationLossyCompressionQuality: 0.82] as CFDictionary)
    if !CGImageDestinationFinalize(dest) {
        FileHandle.standardError.write("failed page \(i+1)\n".data(using:.utf8)!); exit(1)
    }
    print("\(out.lastPathComponent) \(w)x\(h)")
}
