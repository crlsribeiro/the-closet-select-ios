import Testing
@testable import TheClosetSelect

@Suite("AppEnvironment")
struct AppEnvironmentTests {
    @Test(
        "Given a known value in Info.plist, then the matching environment is used",
        arguments: [("dev", AppEnvironment.dev), ("qa", .qa), ("prod", .prod), ("QA", .qa)]
    )
    func readsKnownValue(raw: String, expected: AppEnvironment) {
        let environment = AppEnvironment.from(infoDictionary: ["AppEnvironment": raw])

        #expect(environment == expected)
    }

    static let invalidInfo: [[String: any Sendable]?] = [
        nil,
        [:],
        ["AppEnvironment": "staging"],
        ["AppEnvironment": 42]
    ]

    @Test("Given a missing or unknown value, then it falls back to production", arguments: invalidInfo)
    func fallsBackToProduction(info: [String: any Sendable]?) {
        let dictionary = info.map { $0 as [String: Any] }

        #expect(AppEnvironment.from(infoDictionary: dictionary) == .prod)
    }

    @Test("Only Dev and QA builds show a badge")
    func onlyNonProductionShowsBadge() {
        #expect(AppEnvironment.dev.badgeTitle == "DEV")
        #expect(AppEnvironment.qa.badgeTitle == "QA")
        #expect(AppEnvironment.prod.badgeTitle == nil)
    }

    @Test("The Dev test scheme runs with the Dev environment")
    func devSchemeUsesDevEnvironment() {
        #expect(AppEnvironment.current == .dev)
    }
}
