# Amazon Q Developer: Features and Capabilities (2025)

## Overview

Amazon Q Developer (formerly Amazon CodeWhisperer) is AWS's AI-powered coding assistant that includes real-time code suggestions, security scanning, and autonomous agent capabilities. CodeWhisperer features are now integrated into the expanded Q Developer platform.

## Pricing Plans (2025)

### Free Tier
- Perpetual free access for individuals
- Maintains CodeWhisperer individual tier availability
- Basic code completion features

### Pro Plan
- $19/user/month
- 1,000 agentic requests per month
- 4,000 lines of code generation per month
- Premium features and agent access

## Key Features and Capabilities

### Core Coding Features
- Real-time code suggestions in IDEs
- Security scans flagging risks including hardcoded secrets, SQL injection, bad patterns
- Open source reference tracking identifying code origin
- Support for all major and emerging programming languages:
  - Python
  - Java
  - TypeScript
  - C
  - Rust
  - Additional languages

### Autonomous Agents
- Multi-step task handling for complex operations
- Feature implementation capabilities
- Code refactoring automation
- Dependency upgrades
- Q Developer analyzes app code
- Generates necessary new code
- Creates step-by-step execution plans
- Tests code before implementation
- Executes proposed changes

### AWS-Specific Capabilities
- AWS SDK recognition in developer code
- Contextual recommendations based on AWS SDKs
- Account-level AWS queries directly from IDE
- Enhanced recommendations for AWS services

### Security and Compliance
- Built-in security scanner for code vulnerabilities
- Open source reference tracking for transparency
- SOC, ISO, HIPAA, and PCI compliance

## IDE Support

- VS Code integration
- JetBrains IDEs compatibility
- Visual Studio support
- Eclipse support
- Local IDE development environment

## Security Features (Pro Plan)

- Data isolation: no training on user inputs
- IP indemnity protection
- Single Sign-On (SSO) support via IAM Identity Center

## Strengths

- Perpetual free tier with no expiration
- AWS ecosystem integration provides cloud-native advantages
- Security-first approach with built-in vulnerability scanning
- Open source reference tracking for transparency
- Compliant with major security standards
- Strong enterprise security features on Pro plan
- Multi-IDE support covers most developer environments

## Weaknesses and Limitations

- Agent capabilities require Pro tier subscription
- Less deep codebase context understanding compared to Cursor or Claude
- AWS-focused recommendations may be less useful for non-AWS projects
- Smaller ecosystem compared to GitHub Copilot
- Limited multi-file awareness in base code completion
- Requires AWS tooling knowledge for optimal AWS-specific features
- Agent execution may be slower than some competitors
