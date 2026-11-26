import Testing
@testable import Core

@Suite("ViewState")
struct ViewStateTests {
    @Test("Given a loaded state, then its value is exposed")
    func loadedStateExposesValue() {
        let state = ViewState.loaded(3)

        #expect(state.value == 3)
    }

    @Test(
        "Given a state that is not loaded, then it has no value",
        arguments: [ViewState<Int>.idle, .loading, .empty, .failed(.network)]
    )
    func notLoadedStateHasNoValue(state: ViewState<Int>) {
        #expect(state.value == nil)
    }

    @Test("Given a loading state, then isLoading is true")
    func loadingStateIsLoading() {
        #expect(ViewState<Int>.loading.isLoading)
    }

    @Test(
        "Given a state that is not loading, then isLoading is false",
        arguments: [ViewState<Int>.idle, .loaded(1), .empty, .failed(.unknown)]
    )
    func otherStatesAreNotLoading(state: ViewState<Int>) {
        #expect(!state.isLoading)
    }

    @Test("Given a failed state, then its error is exposed")
    func failedStateExposesError() {
        let state = ViewState<Int>.failed(.unauthorized)

        #expect(state.error == .unauthorized)
    }
}
