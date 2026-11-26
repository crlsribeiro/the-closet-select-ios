import Foundation
import Testing

/// Bug: the app launched to a black screen because the generated Info.plist
/// had no scene manifest, so the SwiftUI window was never created.
@Suite("Launch configuration · Regressions")
struct LaunchConfigurationRegressionTests {
    private let info = Bundle.main.infoDictionary ?? [:]

    @Test("Info.plist declares a scene manifest so SwiftUI can create its window", .tags(.regression))
    func declaresSceneManifest() {
        #expect(info["UIApplicationSceneManifest"] is [String: Any])
    }

    @Test("Info.plist declares a launch screen", .tags(.regression))
    func declaresLaunchScreen() {
        #expect(info["UILaunchScreen"] is [String: Any])
    }
}
