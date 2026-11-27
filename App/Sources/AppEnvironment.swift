import Foundation

/// The environment this build belongs to, read from the `AppEnvironment` Info.plist key
/// that each `.xcconfig` (Dev, QA, Prod) sets.
enum AppEnvironment: String, Sendable, CaseIterable {
    case dev
    case qa
    case prod

    static var current: AppEnvironment {
        from(infoDictionary: Bundle.main.infoDictionary)
    }

    /// Missing or unknown values fall back to `.prod`, so a misconfigured build never shows debug UI.
    static func from(infoDictionary: [String: Any]?) -> AppEnvironment {
        guard let raw = infoDictionary?["AppEnvironment"] as? String else {
            return .prod
        }
        return AppEnvironment(rawValue: raw.lowercased()) ?? .prod
    }

    /// Dev and QA builds show a small badge so testers always know which app they are using.
    var badgeTitle: String? {
        switch self {
        case .dev: "DEV"
        case .qa: "QA"
        case .prod: nil
        }
    }
}
