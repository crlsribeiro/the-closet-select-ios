#!/usr/bin/env bash
# Converts an Xcode .xcresult bundle into SonarQube generic coverage XML.
# Usage: scripts/coverage/xccov-to-sonar.sh TestResults.xcresult > coverage/app.xml
set -euo pipefail

xcresult="$1"
repo_root="$(pwd -P)"

# Refuse results outside the repository (path traversal).
xcresult_dir="$(cd "$(dirname "$xcresult")" && pwd -P)"
case "$xcresult_dir/" in
    "$repo_root"/*) ;;
    *) echo "error: $xcresult is outside the repository" >&2; exit 1 ;;
esac

echo '<coverage version="1">'
xcrun xccov view --archive --file-list "$xcresult" | while read -r file; do
    case "$file" in
        "$repo_root"/App/*|"$repo_root"/Packages/*/Sources/*) ;;
        *) continue ;;
    esac
    echo "  <file path=\"${file#"$repo_root"/}\">"
    xcrun xccov view --archive --file "$file" "$xcresult" | sed -n \
        -e 's/^ *\([0-9][0-9]*\): 0.*$/    <lineToCover lineNumber="\1" covered="false"\/>/p' \
        -e 's/^ *\([0-9][0-9]*\): [1-9].*$/    <lineToCover lineNumber="\1" covered="true"\/>/p'
    echo '  </file>'
done
echo '</coverage>'
