import Testing

extension Tag {
    /// Tests that reproduce a reported bug. They are never removed.
    @Tag static var regression: Self
    /// Tests that implement a Gherkin scenario from `docs/features`.
    @Tag static var acceptance: Self
}
