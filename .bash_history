            
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: App-Ready-For-Testing
          path: App.xcarchive
EOF

git add .
git commit -m "Fix: Forcing folder wipe and scheme injection"
git push origin main
cat << 'EOF' > .github/workflows/build-v1.yml
name: App Store Build
on: [push]
jobs:
  build:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install Dependencies
        run: npm install --legacy-peer-deps

      - name: Build Web Assets
        run: npm run build
        env:
          VITE_GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}

      - name: Reset & Sync Capacitor
        run: |
          rm -rf ios
          npx cap add ios
          npx cap sync ios

      - name: Force Share Scheme
        run: |
          ruby -e '
          require "fileutils"
          path = "ios/App/App.xcodeproj/xcshareddata/xcschemes"
          FileUtils.mkdir_p(path)
          scheme_content = %Q{<?xml version="1.0" encoding="UTF-8"?>
          <Scheme LastUpgradeVersion="1600">
            <BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES">
              <BuildActionEntries>
                <BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">
                  <BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="App" BlueprintName="App" ReferencedContainer="container:App.xcodeproj"></BuildableReference>
                </BuildActionEntry>
              </BuildActionEntries>
            </BuildAction>
          </Scheme>}
          File.write("#{path}/App.xcscheme", scheme_content)
          puts "Shared scheme created at #{path}"'

      - name: Build Archive
        run: |
          xcodebuild archive \
            -project ios/App/App.xcodeproj \
            -scheme App \
            -configuration Debug \
            -destination 'generic/platform=iOS' \
            -archivePath App.xcarchive \
            CODE_SIGNING_ALLOWED=NO \
            CODE_SIGNING_REQUIRED=NO \
            CODE_SIGN_IDENTITY="" \
            AD_HOC_CODE_SIGNING_ALLOWED=YES

      - name: Export IPA
        run: |
          # This extracts the .app from the archive and prepares it for a simulator or jailbroken/dev device
          mkdir -p Payload
          cp -r App.xcarchive/Products/Applications/App.app Payload/
          zip -r App.ipa Payload
          
      - name: Upload IPA
        uses: actions/upload-artifact@v4
        with:
          name: iPhone-Installable-App
          path: App.ipa
EOF

git add .
git commit -m "Action: Automating IPA export"
git push origin main
# Target the Simulator instead of a physical device
xcodebuild build   -project ios/App/App.xcodeproj   -scheme App   -configuration Debug   -destination 'platform=iOS Simulator,name=iPhone 15'   -derivedDataPath build
cat << 'EOF' > .github/workflows/build-v1.yml
name: App Store Build
on: [push]
jobs:
  build:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install Dependencies
        run: npm install --legacy-peer-deps

      - name: Build Web Assets
        run: npm run build
        env:
          VITE_GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}

      - name: Reset & Sync Capacitor
        run: |
          rm -rf ios
          npx cap add ios
          npx cap sync ios

      - name: Force Share Scheme
        run: |
          ruby -e '
          require "fileutils"
          path = "ios/App/App.xcodeproj/xcshareddata/xcschemes"
          FileUtils.mkdir_p(path)
          scheme_content = %Q{<?xml version="1.0" encoding="UTF-8"?>
          <Scheme LastUpgradeVersion="1600">
            <BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES">
              <BuildActionEntries>
                <BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">
                  <BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="App" BlueprintName="App" ReferencedContainer="container:App.xcodeproj"></BuildableReference>
                </BuildActionEntry>
              </BuildActionEntries>
            </BuildAction>
          </Scheme>}
          File.write("#{path}/App.xcscheme", scheme_content)
          puts "Shared scheme created at #{path}"'

      - name: Build Simulator App
        run: |
          # Build specifically for the Simulator (no signing required!)
          xcodebuild build \
            -project ios/App/App.xcodeproj \
            -scheme App \
            -configuration Debug \
            -destination 'platform=iOS Simulator,name=iPhone 16' \
            -derivedDataPath build_output \
            CODE_SIGNING_ALLOWED=NO

      - name: Package for Appetize
        run: |
          # Find the .app folder and zip it
          APP_PATH=$(find build_output/Build/Products/Debug-iphonesimulator -name "*.app" | head -n 1)
          cd $(dirname "$APP_PATH")
          zip -r ../../../appetize_build.zip $(basename "$APP_PATH")

      - name: Upload for Appetize
        uses: actions/upload-artifact@v4
        with:
          name: Appetize-Zip
          path: appetize_build.zip
EOF

git add .
git commit -m "Action: Creating simulator build for Appetize.io"
git push origin main
cd /sdcard/Download
nano ai_girlfriend_video.html
python3 -m http.server 8080
sed -i 's/"Authorization": "Basic " + DID_KEY/"Authorization": "Basic " + btoa(DID_KEY)/' /sdcard/Download/ai_girlfriend_video.html
grep -E "GROQ_KEY|DID_KEY" /sdcard/Download/ai_girlfriend_video.html | head -2
curl -s https://api.groq.com/openai/v1/chat/completions   -H "Authorization: Bearer $(grep 'GROQ_KEY =' /sdcard/Download/ai_girlfriend_video.html | cut -d'"' -f2)"   -H "Content-Type: application/json"   -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' | grep -o '"content":"[^"]*"'
sed -i 's/"Authorization": "Basic " + btoa(DID_KEY)/"Authorization": "Basic " + DID_KEY/' /sdcard/Download/ai_girlfriend_video.html
python3 -m http.server 8080
curl -s -X POST https://api.d-id.com/talks   -H "Authorization: Basic $(grep 'DID_KEY =' /sdcard/Download/ai_girlfriend_video.html | cut -d'"' -f2)"   -H "Content-Type: application/json"   -d '{"source_url":"https://create-images-results.d-id.com/DefaultPresenters/amy-jcwCkrUNRoY/image.jpeg","script":{"type":"text","input":"Hi","provider":{"type":"microsoft","voice_id":"en-US-JennyNeural"}}}' | head -50
curl -X POST https://api.d-id.com/talks   -H "Authorization: Basic $(grep 'DID_KEY =' /sdcard/Download/ai_girlfriend_video.html | cut -d'"' -f2)"   -H "Content-Type: application/json"   -d '{"source_url":"https://create-images-results.d-id.com/DefaultPresenters/amy-jcwCkrUNRoY/image.jpeg","script":{"type":"text","input":"Hi","provider":{"type":"microsoft","voice_id":"en-US-JennyNeural"}}}'
grep 'DID_KEY =' /sdcard/Download/ai_girlfriend_video.html
curl -X POST https://api.d-id.com/talks   -H "Authorization: Basic bWVycml0dGRpZ2l0YWx2ZW50dXJlc0BnbWFpbC5jb206bteZwt0f3TEGSpR99lQAc"   -H "Content-Type: application/json"   -d '{"source_url":"https://create-images-results.d-id.com/DefaultPresenters/amy-jcwCkrUNRoY/image.jpeg","script":{"type":"text","input":"Hi","provider":{"type":"microsoft","voice_id":"en-US-JennyNeural"}}}'
cat << 'EOF' > .github/workflows/build-v1.yml
name: App Store Build
on: [push]
jobs:
  build:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install Dependencies
        run: npm install --legacy-peer-deps

      - name: Build Web Assets
        run: npm run build
        env:
          VITE_GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}

      - name: Reset & Sync Capacitor
        run: |
          rm -rf ios
          npx cap add ios
          npx cap sync ios

      - name: Build Simulator App
        run: |
          # Faster build specifically for Appetize/Simulator
          xcodebuild build \
            -project ios/App/App.xcodeproj \
            -scheme App \
            -configuration Debug \
            -destination 'platform=iOS Simulator,name=iPhone 16' \
            -derivedDataPath build_output \
            CODE_SIGNING_ALLOWED=NO \
            CODE_SIGNING_REQUIRED=NO

      - name: Debug Path Finding
        run: |
          echo "Searching for .app folder..."
          find build_output -name "*.app"
          
      - name: Package for Appetize
        run: |
          # Use find to grab the path even if it's buried
          APP_DIR=$(find build_output -name "App.app" -type d | head -n 1)
          if [ -z "$APP_DIR" ]; then echo "Error: App not found"; exit 1; fi
          zip -r appetize_build.zip "$APP_DIR"

      - name: Upload for Appetize
        uses: actions/upload-artifact@v4
        with:
          name: Appetize-Zip
          path: appetize_build.zip
          if-no-files-found: error
EOF

git add .
git commit -m "Fix: Absolute path finding and build optimization"
git push origin main
# Update the internal package lists
pkg update && pkg upgrade -y
# Reinstall Git and Node.js
pkg install git nodejs -y
# Verify they are back
git --version
node -v
# Move to your home directory
cd ~
# Re-download the project
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git clone https://YOUR_TOKEN@github.com/merrittdigitalventures-arch/YOUR_REPO_NAME.git
git clone https://oauth2:YOUR_TOKEN@github.com/merrittdigitalventures-arch/ai-companion.git
cd ~/ai-companion
termux-wake-lock
ls -a
gh run list --limit 5
gh run download -n Appetize-Zip
gh api repos/merrittdigitalventures-arch/ai-companion/actions/artifacts --jq '.artifacts[].name'
gh run download -n iPhone-Installable-App
ls -F
mv App.ipa appetize_upload.zip
mv appetize_upload.zip /sdcard/Download/
ls /sdcard/Download/appetize_upload.zip
cat << 'EOF' > .github/workflows/build-v1.yml
name: Appetize Simulator Build
on: [push]
jobs:
  build:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install Dependencies
        run: npm install --legacy-peer-deps

      - name: Build Web Assets
        run: npm run build
        env:
          VITE_GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}

      - name: Reset & Sync Capacitor
        run: |
          rm -rf ios
          npx cap add ios
          npx cap sync ios

      - name: Build for Simulator
        run: |
          # This is the magic command for Appetize
          xcodebuild build \
            -project ios/App/App.xcodeproj \
            -scheme App \
            -configuration Debug \
            -sdk iphonesimulator \
            -destination 'platform=iOS Simulator,name=iPhone 16' \
            -derivedDataPath build_output \
            CODE_SIGNING_ALLOWED=NO

      - name: Package for Appetize
        run: |
          # Create a proper ZIP of the .app folder
          cd build_output/Build/Products/Debug-iphonesimulator
          zip -r ../../../appetize_sim_build.zip App.app

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: Simulator-Zip
          path: appetize_sim_build.zip
EOF

git add .
git commit -m "Fix: Explicitly targeting iphonesimulator SDK"
git push origin main
# Untrack the folders that are causing the 'embedded' error
git rm -r --cached jongpt
git rm -r --cached ai-companion
# Find and delete all hidden .git folders EXCEPT the main one in your root
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} +
# Rename current branch to main (if it's currently master)
git branch -M main
# Add all files now that the embedded repos are gone
git add .
# Create the first commit
git commit -m "Fix: Unified repository and added simulator build workflow"
git push -u origin main
# 1. Untrack the folders that are acting like "embedded" repos
git rm -r --cached jongpt
git rm -r --cached ai-companion
# 2. Delete the internal hidden .git folders (the "ghost brains")
# This ensures they become regular folders your main project can see
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} +
# 3. Add everything to your staging area
git add .
# 4. Create your first real commit
git commit -m "Fix: Unified project and added simulator build workflow"
git rm -r --cached jongpt
git rm -r --cached ai-companion
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} +
# 1. Stage every file in the directory
git add .
# 2. Name your branch 'main' (modern standard)
git branch -M main
# 3. Create the commit message
git commit -m "Fix: Unified folders and added simulator build workflow"
git push -u origin main
# 1. Reset the index so Git "forgets" the broken folder links
git rm -r --cached .
# 2. Kill the hidden .git folders inside your sub-folders
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} +
# 3. Re-add everything (it should take a second as it processes files)
git add .
git commit -m "Fix: Unified repository and simulator workflow"
# 1. Reset the index so Git "forgets" the broken folder links
git rm -r --cached .
# 2. Kill the hidden .git folders inside your sub-folders
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} +
# 3. Re-add everything (it should take a second as it processes files)
git add .
git commit -m "Fix: Unified repository and simulator workflow"
git push https://YOUR_TOKEN@github.com/merrittdigitalventures-arch/ai-companion.git main
git remote remove origin
git remote add origin https://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@github.com/merrittdigitalventures-arch/ai-companion.git
git push -u origin main
# 1. Force Git to forget the 'embedded' folder links
git rm -r --cached .
# 2. Delete hidden .git folders inside subdirectories
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} +
# 3. Add and commit everything properly (you should see a long list of files now)
git add .
git commit -m "Final Fix: Unified repo and Simulator build"
# 4. Push using the Token-in-URL method (The 'Magic' Command)
git push https://PASTE_YOUR_TOKEN_HERE@github.com/merrittdigitalventures-arch/ai-companion.git main
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main
# Pull the changes from GitHub and combine them with your local ones
git pull https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --rebase
# Now push again
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main
git rebase --abort
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
echo "node_modules/
dist/
build/
.expo/
ios/build/
ios/DerivedData/" > .gitignore
git rm -r --cached .
git add .
git commit -m "Optimize: Removed heavy files for faster push"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
echo "node_modules/
venv/
__pycache__/
.expo/
ios/build/
ios/DerivedData/
dist/
build/" > .gitignore
git rm -r --cached .
git add .
git commit -m "Optimize: stripped heavy files for fast push"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
echo "node_modules/
venv/
.expo/
ios/build/
ios/DerivedData/
build/
dist/" > .gitignore
git rm -r --cached .
git add .
git commit -m "Fix: Stripped heavy files and updated simulator workflow"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
# Force Git to forget the 31,000 files
git rm -r --cached .
# Create the ignore list (this is the most important part)
echo "node_modules/
venv/
.expo/
ios/build/
ios/DerivedData/
build/
dist/
__pycache__/" > .gitignore
# Add back only the clean files
git add .
git commit -m "Final Fix: Lightweight simulator build"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
git rm -r --cached
bash
echo "node_modules/
venv/
.expo/
ios/build/
ios/DerivedData/
build/
dist/
pycache/" > .gitignore
git add .
git commit -m "Emergency Fix: Cleaned repo for simulator build"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
git rm -r --cached .
echo "node_modules/
venv/
.expo/
ios/build/
ios/DerivedData/
build/
dist/
__pycache__/" > .gitignore
git add .
git commit -m "Fast Fix: Cleaned repo for simulator"
git add .
git commit -m "Fast Fix: Cleaned repo for simulator"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
git add .
git commit -m "Cleanup: Removing 31,000 heavy files"
git reset --soft HEAD~1
git add .
git commit -m "Final: Lightweight simulator build"
git push https://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@github.com/merrittdigitalventures-arch/ai-companion.git main --force
rm -rf .git
git init
echo "node_modules/
venv/
.expo/
ios/build/
ios/DerivedData/
build/
dist/
__pycache__/" > .gitignore
git add .
git commit -m "Fresh start: Clean simulator build"
git remote add origin https://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@github.com/merrittdigitalventures-arch/ai-companion.git
git push -u origin main --force
git add .
git commit -m "Fresh start: Clean simulator build"
git remote add origin https://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@github.com/merrittdigitalventures-arch/ai-companion.git
git push -u origin main --force
git branch -M main
git add .
git commit -m "Final cleanup for simulator build"
git push -u origin main --force
rm -rf .git
git init
git branch -M main
echo "node_modules/
venv/
.expo/
ios/build/
ios/DerivedData/
build/
dist/
__pycache__/" > .gitignore
git add .
git commit -m "Fresh start: Clean simulator build"
git remote add origin https://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@github.com/merrittdigitalventures-arch/ai-companion.git
git push -u origin main --force
