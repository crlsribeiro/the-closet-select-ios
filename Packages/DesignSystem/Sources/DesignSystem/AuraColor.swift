#if canImport(SwiftUI)
import SwiftUI

public extension Color {
    init(hex: UInt32, opacity: Double = 1) {
        let rgb = RGB(hex: hex)
        self.init(.sRGB, red: rgb.red, green: rgb.green, blue: rgb.blue, opacity: opacity)
    }
}

/// SwiftUI colors for the brand tokens in `AuraPalette`.
public enum AuraColor {
    public static let background = Color(hex: AuraPalette.background)
    public static let surface = Color(hex: AuraPalette.surface)
    public static let surfaceRaised = Color(hex: AuraPalette.surfaceRaised)
    public static let gold = Color(hex: AuraPalette.gold)
    public static let onGold = Color(hex: AuraPalette.onGold)
    public static let textPrimary = Color(hex: AuraPalette.textPrimary)
    public static let textSecondary = Color(hex: AuraPalette.textSecondary)
}
#endif
