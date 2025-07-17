# Contributing to StorjLedger

Thank you for considering contributing to **StorjLedger**! We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code enhancements. Please follow the guidelines below to streamline the contribution process.

---

## 1. Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful, inclusive, and constructive.

## 2. Getting Started

1. **Fork the repository**  
   Click the “Fork” button at https://github.com/SahaReno/StorjLedger to create your own copy.

2. **Clone your fork**  
   ```bash
   git clone https://github.com/<your-username>/StorjLedger.git
   cd StorjLedger
   ```

3. **Set up upstream remote**  
   ```bash
   git remote add upstream https://github.com/SahaReno/StorjLedger.git
   git fetch upstream
   ```

4. **Install dependencies**  
   - **Go Services**:  
     ```bash
     cd go-services
     go mod download
     ```
   - **Node.js CLI/SDK**:  
     ```bash
     cd cli-sdk
     npm install
     ```

## 3. Branching Strategy

We follow the GitHub Flow model:

- Create feature branches off `main` for new work:  
  ```bash
  git checkout main
  git pull upstream main
  git checkout -b feature/awesome-feature
  ```
- Keep branches focused: one feature or fix per branch.
- Regularly sync with `main` to avoid conflicts:
  ```bash
  git fetch upstream
  git checkout main
  git merge upstream/main
  git push
  ```

## 4. Commit Message Guidelines

- Use the [Conventional Commits](https://www.conventionalcommits.org/) format:
  ```
  <type>(<scope>): <short description>

  [optional body]

  [optional footer]
  ```
- **Types**:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `docs`: Documentation only changes
  - `style`: Formatting, missing semicolons, etc.
  - `refactor`: Code change that neither fixes a bug nor adds a feature
  - `test`: Adding or updating tests
  - `chore`: Maintenance tasks
- Keep the subject line <= 72 characters.

## 5. Pull Request Process

1. **Push your branch**  
   ```bash
   git push origin feature/awesome-feature
   ```

2. **Open a Pull Request**  
   - Target branch: `main`
   - Provide a descriptive title and summary.
   - Link any relevant issues (e.g., “Fixes #123”).

3. **Review & Feedback**  
   - A maintainer will review your PR.
   - Address review comments promptly.
   - Update your branch if the base branch changes.

4. **Merge**  
   Once approved, a maintainer will squash and merge your PR to keep history clean.

## 6. Reporting Issues

- Check existing issues first to avoid duplicates.
- Use the issue template and include:
  - **Title**: Clear and descriptive.
  - **Description**: What happened and why it’s a problem.
  - **Steps to Reproduce**: Exact steps to trigger the issue.
  - **Environment**: OS, Docker version, Go/Node versions, etc.
  - **Logs/Output**: Error messages or stack traces.

## 7. Coding Standards & Testing

- **Go**:
  - Follow `golangci-lint` rules.
  - Write unit tests alongside code (`_test.go`).
  - Run tests with:
    ```bash
    go test ./...
    ```
- **Node.js**:
  - Use ESLint with the project’s config.
  - Write tests using Jest.
  - Run tests with:
    ```bash
    npm test
    ```

## 8. Documentation

- Documentation lives under `docs/`.
- Use Markdown (.md) format.
- For architecture or design docs, include diagrams in `docs/assets/`.

## 9. Style & Formatting Tools

- **Go**:
  - `gofmt` for formatting.
  - `golangci-lint run` for linting.
- **JavaScript/TypeScript**:
  - `prettier --write .`
  - `eslint --fix .`

## 10. Thank You!

Your contributions help make StorjLedger better for everyone. If you have questions, feel free to open an issue or join the discussion.

---

*This document was generated automatically. Last updated: July 17, 2025.*
