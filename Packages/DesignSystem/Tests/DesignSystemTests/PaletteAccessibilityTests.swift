import Testing
@testable import DesignSystem

/// WCAG 2.2: normal text needs at least 4.5:1 against its background.
@Suite("Palette accessibility")
struct PaletteAccessibilityTests {
    static let textTokens: [(name: String, hex: UInt32)] = [
        ("textPrimary", AuraPalette.textPrimary),
        ("textSecondary", AuraPalette.textSecondary),
        ("gold", AuraPalette.gold)
    ]

    static let backgrounds: [UInt32] = [
        AuraPalette.background,
        AuraPalette.surface,
        AuraPalette.surfaceRaised
    ]

    @Test(
        "Every text color passes WCAG AA on every dark surface",
        arguments: textTokens, backgrounds
    )
    func textPassesContrast(token: (name: String, hex: UInt32), background: UInt32) {
        let ratio = RGB(hex: token.hex).contrastRatio(with: RGB(hex: background))

        #expect(ratio >= 4.5, "\(token.name) has \(ratio):1")
    }

    @Test("Text on the gold button passes WCAG AA")
    func textOnGoldButtonPassesContrast() {
        let ratio = RGB(hex: AuraPalette.onGold).contrastRatio(with: RGB(hex: AuraPalette.gold))

        #expect(ratio >= 4.5)
    }
}
