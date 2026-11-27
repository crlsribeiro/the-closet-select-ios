import DesignSystem
import SwiftUI

/// Temporary root screen for Sprint 0. It proves the environment setup,
/// the design system tokens, localization and the glass modifier.
struct RootView: View {
    let environment: AppEnvironment

    var body: some View {
        ZStack {
            AuraColor.background.ignoresSafeArea()

            VStack(spacing: 16) {
                Image(systemName: "hanger")
                    .font(.system(size: 56, weight: .thin))
                    .foregroundStyle(AuraColor.gold)
                    .accessibilityHidden(true)

                Text(verbatim: "THE CLOSET SELECT")
                    .font(.system(.title, design: .serif, weight: .semibold))
                    .tracking(4)
                    .foregroundStyle(AuraColor.textPrimary)

                Text("root.tagline")
                    .font(.subheadline)
                    .foregroundStyle(AuraColor.textSecondary)
            }

            if let badge = environment.badgeTitle {
                Text(verbatim: badge)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(AuraColor.gold)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 6)
                    .auraGlass()
                    .frame(maxHeight: .infinity, alignment: .top)
                    .padding(.top, 8)
                    .accessibilityLabel(Text("root.environment \(badge)"))
            }
        }
    }
}

#Preview("Dev") {
    RootView(environment: .dev)
}

#Preview("Prod") {
    RootView(environment: .prod)
}
