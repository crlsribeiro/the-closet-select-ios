import Testing
@testable import Core

@Suite("AppError")
struct AppErrorTests {
    @Test(
        "Every error has a localization key in the error namespace",
        arguments: AppError.allCases
    )
    func everyErrorHasLocalizationKey(error: AppError) {
        #expect(error.localizationKey.hasPrefix("error."))
    }

    @Test("Localization keys are unique")
    func localizationKeysAreUnique() {
        let keys = AppError.allCases.map(\.localizationKey)

        #expect(Set(keys).count == keys.count)
    }
}
