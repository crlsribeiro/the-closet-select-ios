#if canImport(SwiftUI)
import SwiftUI

public extension View {
    /// Glass background with progressive enhancement:
    /// Liquid Glass on iOS 26 and later, a frosted material on iOS 18.
    /// This is the only place in the app that checks for Liquid Glass availability.
    @ViewBuilder
    func auraGlass(in shape: some Shape = Capsule()) -> some View {
        #if compiler(>=6.2)
        if #available(iOS 26, macOS 26, *) {
            glassEffect(.regular, in: shape)
        } else {
            background(.ultraThinMaterial, in: shape)
        }
        #else
        background(.ultraThinMaterial, in: shape)
        #endif
    }
}
#endif
