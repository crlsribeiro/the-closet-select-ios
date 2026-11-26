#if canImport(SwiftUI)
import SwiftUI

public extension View {
    /// Shows the view as a skeleton placeholder with a gold shimmer.
    /// Use the real component with placeholder data so the layout does not jump.
    func skeleton(isActive: Bool) -> some View {
        modifier(SkeletonModifier(isActive: isActive))
    }
}

struct SkeletonModifier: ViewModifier {
    let isActive: Bool

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var phase: CGFloat = -1

    @ViewBuilder
    func body(content: Content) -> some View {
        if isActive {
            content
                .redacted(reason: .placeholder)
                .overlay {
                    shimmer
                        .mask { content.redacted(reason: .placeholder) }
                }
                .disabled(true)
                .accessibilityHidden(true)
                .onAppear(perform: startShimmer)
        } else {
            content
        }
    }

    private var shimmer: some View {
        GeometryReader { proxy in
            LinearGradient(
                colors: [.clear, AuraColor.gold.opacity(0.16), .clear],
                startPoint: .leading,
                endPoint: .trailing
            )
            .frame(width: proxy.size.width)
            .offset(x: phase * proxy.size.width)
        }
        .opacity(reduceMotion ? 0 : 1)
        .allowsHitTesting(false)
    }

    private func startShimmer() {
        guard !reduceMotion else { return }
        phase = -1
        withAnimation(.easeInOut(duration: 1.4).repeatForever(autoreverses: false)) {
            phase = 1
        }
    }
}
#endif
