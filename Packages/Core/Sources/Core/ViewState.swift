/// The single source of truth for what a screen shows.
/// Every View renders all five cases: idle, loading (skeleton), loaded, empty and failed.
public enum ViewState<Value: Sendable>: Sendable {
    case idle
    case loading
    case loaded(Value)
    case empty
    case failed(AppError)

    public var value: Value? {
        if case let .loaded(value) = self {
            return value
        }
        return nil
    }

    public var isLoading: Bool {
        if case .loading = self {
            return true
        }
        return false
    }

    public var error: AppError? {
        if case let .failed(error) = self {
            return error
        }
        return nil
    }
}

extension ViewState: Equatable where Value: Equatable {}
