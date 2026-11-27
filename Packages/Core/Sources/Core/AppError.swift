/// Errors that a screen can show to the user.
/// The text for each case lives in the String Catalog under `localizationKey`.
public enum AppError: Error, Equatable, Sendable, CaseIterable {
    case network
    case unauthorized
    case notFound
    case unknown

    public var localizationKey: String {
        switch self {
        case .network: "error.network"
        case .unauthorized: "error.unauthorized"
        case .notFound: "error.notFound"
        case .unknown: "error.unknown"
        }
    }
}
