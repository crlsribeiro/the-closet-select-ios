import Testing
@testable import DesignSystem

@Suite("RGB")
struct RGBTests {
    @Test("Given a hex value, then each channel is split from 0 to 1")
    func splitsHexIntoChannels() {
        let gold = RGB(hex: 0xD4AF37)

        #expect(gold.red == 212.0 / 255.0)
        #expect(gold.green == 175.0 / 255.0)
        #expect(gold.blue == 55.0 / 255.0)
    }

    @Test("Black on white has the maximum contrast ratio of 21:1")
    func blackOnWhiteIsMaximumContrast() {
        let ratio = RGB(hex: 0x000000).contrastRatio(with: RGB(hex: 0xFFFFFF))

        #expect(abs(ratio - 21) < 0.01)
    }

    @Test("Contrast ratio does not depend on the order of the colors")
    func contrastIsSymmetric() {
        let gold = RGB(hex: 0xD4AF37)
        let black = RGB(hex: 0x0B0B0B)

        #expect(gold.contrastRatio(with: black) == black.contrastRatio(with: gold))
    }
}
