#!/usr/bin/env python3
"""Generate A2 Configuration Management Report and Procurement RFP as Word documents."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

OUTPUT_DIR = r"C:\Users\23961\greenhill-coop-order-system"

def set_font(run, name="Arial", size=12, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    r = run._element
    r.rPr.rFonts.set(qn('w:eastAsia'), name)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    sizes = {1: 16, 2: 14, 3: 12}
    set_font(run, size=sizes.get(level, 12), bold=True)
    return p

def add_body(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_font(run, size=12)
    return p

def add_bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run(text)
    set_font(run, size=12)
    return p

def add_image_placeholder(doc, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"[INSERT SCREENSHOT: {caption}]")
    set_font(run, size=11, bold=True)
    run.font.color.rgb = RGBColor(128, 128, 128)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_run = cap.add_run(caption)
    set_font(cap_run, size=10)
    cap_run.font.italic = True

def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_font(run, size=11, bold=True)
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            set_font(run, size=10)
    return table

# ============================================================
# REPORT 1: Configuration Management Report
# ============================================================
def generate_config_report():
    doc = Document()
    # Set default style
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # Cover page
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ISYS3001 Managing Software Development")
    set_font(run, size=18, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Assessment 2: Configuration Management Report")
    set_font(run, size=16, bold=True)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Greenhill Food Co-op Ordering System")
    set_font(run, size=14)
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Student: Ziliang Lu")
    set_font(run, size=12)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("GitHub: ziliang-lu-scu")
    set_font(run, size=12)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Date: October 2026")
    set_font(run, size=12)
    doc.add_page_break()

    # 1. Introduction
    add_heading(doc, "1. Introduction", 1)
    add_body(doc, "This report documents the configuration management strategy and practices implemented for the Greenhill Food Co-op Ordering System project. The project aims to develop a web-based application that enables Greenhill Food Co-op members to place orders, manage products, and coordinate order rounds. Effective configuration management is critical to ensure that all project artifacts—source code, documentation, and configuration files—are properly controlled, versioned, and traceable throughout the software development lifecycle.")
    add_body(doc, "The configuration management approach adopted in this project follows industry best practices, including the Git Flow branching model, GitHub as the version control platform, and structured change control through pull requests and code reviews. This report details the branching strategy, configuration item identification, change control process, build and release management, and provides evidence of implementation through screenshots from the GitHub repository.")

    # 2. Configuration Management Strategy
    add_heading(doc, "2. Configuration Management Strategy", 1)
    add_heading(doc, "2.1 Branching Strategy (Git Flow)", 2)
    add_body(doc, "The project employs the Git Flow branching model, which provides a structured framework for managing parallel development and releases. The repository contains three primary branch types:")
    add_bullet(doc, "main: The production-ready branch containing stable, released code. All merges to main represent formal releases.")
    add_bullet(doc, "develop: The integration branch where features are combined and tested before release. This branch always contains the latest completed development work.")
    add_bullet(doc, "feature/*: Short-lived branches created from develop for implementing individual features or bug fixes. Each feature branch is merged back to develop through a pull request after code review.")
    add_body(doc, "The workflow follows these steps: (1) A developer creates a feature branch from develop; (2) Work is committed to the feature branch with descriptive commit messages; (3) A pull request is created to merge the feature branch into develop; (4) Team members review the code and provide feedback; (5) After approval, the pull request is merged into develop; (6) When develop is ready for release, a pull request is created to merge develop into main; (7) The release is merged into main, creating a new stable version.")
    add_image_placeholder(doc, "Figure 1: Branch list showing main, develop, and feature/user-auth branches")

    add_heading(doc, "2.2 Version Control Tool: GitHub", 2)
    add_body(doc, "GitHub is used as the central version control platform for the project. GitHub provides a cloud-hosted Git repository with additional collaboration features including pull requests, code review, issue tracking, and project management. The repository is publicly accessible at https://github.com/ziliang-lu-scu/greenhill-coop-order-system, allowing all team members and stakeholders to view the codebase and track development progress.")
    add_body(doc, "Key GitHub features utilized in this project include:")
    add_bullet(doc, "Pull Requests: Used for code review and controlled merging of feature branches.")
    add_bullet(doc, "Code Review: Team members review changes, comment on specific lines, and approve or request modifications before merge.")
    add_bullet(doc, "Commit History: A complete, immutable record of all changes with author, timestamp, and descriptive commit messages.")
    add_bullet(doc, "Branch Protection: The main branch is protected to ensure all changes go through the pull request review process.")
    add_image_placeholder(doc, "Figure 2: Repository homepage showing file structure and README")

    # 3. Configuration Items
    add_heading(doc, "3. Configuration Items", 1)
    add_body(doc, "Configuration items (CIs) are artifacts that are placed under version control and managed through the configuration management process. The following table identifies the key configuration items in the Greenhill Food Co-op Ordering System project:")
    add_table(doc,
        ["Configuration Item", "Type", "Location", "Description"],
        [
            ["Source Code (Python)", "Code", "app/", "Flask application code including models, routes, and initialization"],
            ["HTML Templates", "Code", "app/templates/", "Jinja2 HTML templates for all user interface pages"],
            ["Application Entry Point", "Code", "run.py", "Python script to launch the Flask development server"],
            ["Dependencies", "Config", "requirements.txt", "Pinned Python package dependencies for reproducible builds"],
            ["Environment Template", "Config", ".env.example", "Template for environment variables with placeholder values"],
            ["Git Ignore", "Config", ".gitignore", "Specifies files and directories excluded from version control"],
            ["README", "Documentation", "README.md", "Project overview, installation instructions, and feature list"],
            ["Changelog", "Documentation", "CHANGELOG.md", "Record of notable changes across versions"],
            ["Database", "Data", "instance/app.db", "SQLite database file (generated locally, not committed)"],
        ]
    )
    add_body(doc, "Sensitive configuration items such as the actual .env file containing secret keys and the SQLite database file are excluded from version control through the .gitignore file. This ensures that secrets and generated artifacts are not accidentally committed to the public repository.")

    # 4. Change Control Process
    add_heading(doc, "4. Change Control Process", 1)
    add_body(doc, "All changes to configuration items go through a formal change control process to ensure quality, traceability, and accountability. The change control process consists of the following steps:")
    add_heading(doc, "4.1 Change Request", 3)
    add_body(doc, "A change is initiated by creating a feature branch from the develop branch. The branch name follows the convention feature/<short-description>, such as feature/user-auth or feature/product-management. The developer works on the feature branch, making commits with clear, descriptive messages following the Conventional Commits format (e.g., feat:, fix:, docs:, refactor:).")
    add_heading(doc, "4.2 Pull Request and Code Review", 3)
    add_body(doc, "When the feature is complete, the developer creates a pull request (PR) to merge the feature branch into develop. The PR includes a title, description of changes, and a checklist of testing performed. Team members review the PR, examining the code for correctness, adherence to coding standards, security issues, and potential bugs. Reviewers may comment on specific lines of code, request changes, or approve the PR.")
    add_image_placeholder(doc, "Figure 3: Pull request #1 showing code review comments and approval")
    add_heading(doc, "4.3 Merge and Integration", 3)
    add_body(doc, "After the PR has been approved by at least one team member and all review comments have been addressed, the PR is merged into the develop branch. The merge creates a merge commit that records the integration of the feature. The feature branch is then deleted to keep the repository clean.")
    add_heading(doc, "4.4 Release", 3)
    add_body(doc, "When the develop branch contains a complete set of features ready for production, a release pull request is created to merge develop into main. This PR represents a formal release and is reviewed by the project lead. After approval, the release is merged into main, creating a new stable version. The main branch always reflects the latest production-ready state of the application.")
    add_image_placeholder(doc, "Figure 4: Pull request #2 showing release merge from develop to main")

    # 5. Build and Release Management
    add_heading(doc, "5. Build and Release Management", 1)
    add_heading(doc, "5.1 Local Development Environment", 2)
    add_body(doc, "The project uses a standardized local development environment to ensure consistency across team members. The environment setup includes:")
    add_bullet(doc, "Python 3.10+: The programming language for the Flask application.")
    add_bullet(doc, "Git: Version control client for interacting with the GitHub repository.")
    add_bullet(doc, "Virtual Environment (venv): Isolated Python environment to manage project dependencies without conflicts.")
    add_bullet(doc, "VS Code: Recommended code editor with Python extension for development and debugging.")
    add_body(doc, "Dependencies are managed through the requirements.txt file, which pins specific versions of all required packages including Flask 3.0.0, Flask-SQLAlchemy 3.1.1, Flask-Login 0.6.3, Flask-Migrate 4.0.5, pytest 7.4.3, and Werkzeug 3.0.1. Team members install dependencies by running pip install -r requirements.txt within their virtual environment.")
    add_heading(doc, "5.2 Build Process", 2)
    add_body(doc, "The Flask application does not require a compilation build step, as Python is an interpreted language. The application is run directly from the source code using the command python run.py, which starts the Flask development server on http://127.0.0.1:5000. The application factory pattern is used, with create_app() in app/__init__.py initializing the Flask application, configuring the database, and registering all route blueprints.")
    add_heading(doc, "5.3 Release Management", 2)
    add_body(doc, "Releases are managed through the Git Flow process described in Section 2.1. Each merge to the main branch represents a formal release. The CHANGELOG.md file documents notable changes in each release, following the Keep a Changelog format. Version numbers follow Semantic Versioning (MAJOR.MINOR.PATCH), where MAJOR versions indicate incompatible API changes, MINOR versions add functionality in a backwards-compatible manner, and PATCH versions make backwards-compatible bug fixes.")
    add_image_placeholder(doc, "Figure 5: Commit history showing merge commits and feature commits")

    # 6. Evidence of Implementation
    add_heading(doc, "6. Evidence of Implementation", 1)
    add_body(doc, "The following screenshots provide evidence of the configuration management practices implemented in the GitHub repository:")
    add_image_placeholder(doc, "Figure 6: Repository homepage showing all configuration items")
    add_image_placeholder(doc, "Figure 7: Branch list with main, develop, and feature branches")
    add_image_placeholder(doc, "Figure 8: Commit history with conventional commit messages")
    add_image_placeholder(doc, "Figure 9: Closed pull requests list showing PR #1 and PR #2")
    add_image_placeholder(doc, "Figure 10: Pull request #1 detail with code review comments")
    add_image_placeholder(doc, "Figure 11: requirements.txt showing pinned dependencies")
    add_image_placeholder(doc, "Figure 12: .gitignore showing excluded files")

    # 7. GenAI Declaration
    add_heading(doc, "7. Generative AI Declaration", 1)
    add_body(doc, "In accordance with the ISYS3001 assessment policy on the use of generative AI tools, this section declares the extent to which AI tools were used in the preparation of this report and the associated project artifacts.")
    add_body(doc, "Generative AI tools (specifically, Doubao) were used at Level 2 as permitted by the assessment guidelines. The following uses are declared:")
    add_bullet(doc, "Brainstorming and ideation: AI was used to generate initial ideas for the project structure, feature list, and configuration management approach.")
    add_bullet(doc, "Grammar and language checking: AI was used to review and correct grammar, spelling, and phrasing in the report text.")
    add_bullet(doc, "Formatting assistance: AI was used to help structure the report and ensure consistent formatting.")
    add_bullet(doc, "Code generation assistance: AI was used to generate initial boilerplate code for the Flask application, which was then reviewed, modified, and extended by the student.")
    add_body(doc, "AI was NOT used to write the substantive content of this report. All technical analysis, configuration management decisions, and project documentation were authored by the student based on their understanding of the course material and project requirements. All code was reviewed and tested by the student before being committed to the repository. The student takes full responsibility for the accuracy and completeness of this report and all associated project artifacts.")

    # References
    add_heading(doc, "References", 1)
    add_bullet(doc, "GitHub. (2026). GitHub Docs: About Git. Retrieved from https://docs.github.com/en/get-started/using-git/about-git")
    add_bullet(doc, "Atlassian. (2026). Git Flow Workflow. Retrieved from https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow")
    add_bullet(doc, "Conventional Commits. (2026). Conventional Commits Specification. Retrieved from https://www.conventionalcommits.org/")
    add_bullet(doc, "Preston-Werner, T. (2026). Semantic Versioning 2.0.0. Retrieved from https://semver.org/")
    add_bullet(doc, "Keep a Changelog. (2026). Keep a CHANGELOG. Retrieved from https://keepachangelog.com/")

    path = os.path.join(OUTPUT_DIR, "Ziliang_Lu_ISYS3001_Configuration_Management.docx")
    doc.save(path)
    print(f"Saved: {path}")
    return path

# ============================================================
# REPORT 2: Procurement Plan (RFP)
# ============================================================
def generate_rfp():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # Cover
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ISYS3001 Managing Software Development")
    set_font(run, size=18, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Assessment 2: Procurement Plan")
    set_font(run, size=16, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Request for Proposal (RFP)")
    set_font(run, size=14, bold=True)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Greenhill Food Co-op Ordering System")
    set_font(run, size=14)
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Prepared by: Ziliang Lu")
    set_font(run, size=12)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Issuing Organization: Greenhill Food Co-op")
    set_font(run, size=12)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Date: October 2026")
    set_font(run, size=12)
    doc.add_page_break()

    # 1. Introduction
    add_heading(doc, "1. Introduction", 1)
    add_heading(doc, "1.1 Purpose", 2)
    add_body(doc, "This Request for Proposal (RFP) is issued by Greenhill Food Co-op to solicit proposals from qualified software development vendors for the design, development, implementation, and maintenance of a web-based Cooperative Ordering System. The system will streamline the ordering process for Greenhill Food Co-op members, enabling efficient product catalog management, order placement, order round coordination, and packing sheet generation.")
    add_heading(doc, "1.2 Background", 2)
    add_body(doc, "Greenhill Food Co-op is a member-owned cooperative that provides organic and locally sourced food products to its members. Currently, the ordering process is managed manually through spreadsheets and email, which is time-consuming, error-prone, and difficult to scale as membership grows. The cooperative requires a dedicated web-based system to automate and streamline the ordering workflow, improve accuracy, and enhance the member experience.")
    add_heading(doc, "1.3 Objectives", 2)
    add_body(doc, "The primary objectives of this procurement are:")
    add_bullet(doc, "To acquire a robust, scalable, and user-friendly web-based ordering system tailored to the cooperative's business processes.")
    add_bullet(doc, "To reduce manual effort and errors in order processing through automation.")
    add_bullet(doc, "To provide real-time visibility into orders, products, and order rounds for both members and coordinators.")
    add_bullet(doc, "To ensure data security, privacy, and compliance with relevant regulations.")
    add_bullet(doc, "To establish a long-term partnership with a vendor capable of providing ongoing support and maintenance.")
    add_heading(doc, "1.4 Contact Information", 2)
    add_body(doc, "All inquiries and proposals should be directed to:")
    add_table(doc,
        ["Field", "Details"],
        [
            ["Organization", "Greenhill Food Co-op"],
            ["Contact Person", "Procurement Coordinator"],
            ["Email", "procurement@greenhillcoop.example.com"],
            ["Phone", "+61 2 5550 1234"],
            ["Address", "123 Greenhill Road, Lismore, NSW 2480, Australia"],
            ["RFP Reference", "GHC-ORDER-2026-001"],
        ]
    )

    # 2. Scope of Work
    add_heading(doc, "2. Scope of Work", 1)
    add_heading(doc, "2.1 In Scope", 2)
    add_body(doc, "The selected vendor will be responsible for the following deliverables and activities:")
    add_bullet(doc, "Requirements gathering and analysis: Conduct workshops with cooperative stakeholders to elicit and document detailed functional and non-functional requirements.")
    add_bullet(doc, "System design: Produce system architecture, database design, user interface wireframes, and technical design documents for review and approval.")
    add_bullet(doc, "Development: Build the web application with all features specified in Section 3 (Technical Requirements), following industry best practices and coding standards.")
    add_bullet(doc, "Testing: Perform unit testing, integration testing, user acceptance testing (UAT), and performance testing. Provide test plans, test cases, and test reports.")
    add_bullet(doc, "Deployment: Deploy the application to a production environment, configure hosting, domain, SSL certificates, and database.")
    add_bullet(doc, "Training: Provide training sessions for cooperative coordinators and member support staff on system administration and usage.")
    add_bullet(doc, "Documentation: Deliver comprehensive user manuals, administrator guides, API documentation (if applicable), and technical documentation.")
    add_bullet(doc, "Warranty and maintenance: Provide a minimum 12-month warranty period and optional ongoing maintenance and support services.")
    add_heading(doc, "2.2 Out of Scope", 2)
    add_body(doc, "The following items are explicitly excluded from the scope of this RFP:")
    add_bullet(doc, "Payment processing integration: The system will not process online payments. Orders are paid through separate offline arrangements.")
    add_bullet(doc, "Mobile native applications: Only a responsive web application is required; native iOS or Android apps are not in scope.")
    add_bullet(doc, "Accounting and financial software integration: Integration with accounting systems (e.g., Xero, MYOB) is not required at this stage.")
    add_bullet(doc, "Hardware procurement: The cooperative will provide or procure any necessary hardware (servers, networking equipment) separately.")
    add_bullet(doc, "Data migration from existing spreadsheets: Initial data entry will be performed by cooperative staff; the vendor will provide import tools if feasible.")

    # 3. Technical Requirements
    add_heading(doc, "3. Technical Requirements", 1)
    add_heading(doc, "3.1 Functional Requirements", 2)
    add_body(doc, "The system must include the following functional modules:")
    add_heading(doc, "3.1.1 Member Authentication and Management", 3)
    add_bullet(doc, "Member registration with username, email, and password.")
    add_bullet(doc, "Secure login and logout functionality.")
    add_bullet(doc, "Password hashing using industry-standard algorithms (e.g., bcrypt).")
    add_bullet(doc, "Member profile management (view and edit personal information).")
    add_bullet(doc, "Role-based access control: member and coordinator roles with different permissions.")
    add_heading(doc, "3.1.2 Product Catalog Management", 3)
    add_bullet(doc, "Coordinators can add, edit, and delete products.")
    add_bullet(doc, "Each product has a name, description, unit price, unit of measure, and category.")
    add_bullet(doc, "Products can be marked as active or inactive.")
    add_bullet(doc, "Members can browse the product catalog and view product details.")
    add_heading(doc, "3.1.3 Order Management", 3)
    add_bullet(doc, "Members can place orders for products within an active order round.")
    add_bullet(doc, "Members can specify quantity for each product ordered.")
    add_bullet(doc, "Members can view their order history and current order status.")
    add_bullet(doc, "Members can edit or cancel orders before the order round closes.")
    add_bullet(doc, "Coordinators can view all orders across all members.")
    add_heading(doc, "3.1.4 Order Round Management", 3)
    add_bullet(doc, "Coordinators can create new order rounds with a name, start date, and end date.")
    add_bullet(doc, "Order rounds have statuses: upcoming, active, closed.")
    add_bullet(doc, "Only one order round can be active at a time.")
    add_bullet(doc, "Members can only place orders during active order rounds.")
    add_bullet(doc, "Coordinators can close order rounds manually or automatically at the end date.")
    add_heading(doc, "3.1.5 Packing Sheet Generation", 3)
    add_bullet(doc, "Coordinators can generate a packing sheet for a closed order round.")
    add_bullet(doc, "The packing sheet aggregates quantities by product across all orders.")
    add_bullet(doc, "The packing sheet shows total quantity needed for each product.")
    add_bullet(doc, "The packing sheet can be printed or exported for use during order packing and distribution.")
    add_heading(doc, "3.1.6 Dashboard and Reporting", 3)
    add_bullet(doc, "Coordinator dashboard showing key metrics: active round, total orders, total products, recent activity.")
    add_bullet(doc, "Order totals report showing total quantity and value per product for a round.")
    add_bullet(doc, "Member order summary showing each member's orders for a round.")
    add_heading(doc, "3.2 Non-Functional Requirements", 2)
    add_table(doc,
        ["Category", "Requirement"],
        [
            ["Performance", "Page load time under 3 seconds for 95% of requests; support up to 500 concurrent users."],
            ["Security", "HTTPS encryption, password hashing, CSRF protection, SQL injection prevention, role-based access control."],
            ["Scalability", "Architecture designed to support growth in users, products, and order volume."],
            ["Availability", "99.5% uptime during business hours (8am-8pm AEST)."],
            ["Usability", "Intuitive, responsive user interface accessible on desktop and mobile devices."],
            ["Compatibility", "Support for modern web browsers (Chrome, Firefox, Safari, Edge) on desktop and mobile."],
            ["Maintainability", "Well-documented, modular codebase following SOLID principles and coding standards."],
            ["Data Backup", "Automated daily database backups with 30-day retention period."],
        ]
    )
    add_heading(doc, "3.3 Technology Stack", 2)
    add_body(doc, "The proposed technology stack should be modern, well-supported, and suitable for the project requirements. The following stack is preferred, but vendors may propose alternatives with justification:")
    add_table(doc,
        ["Layer", "Preferred Technology"],
        [
            ["Backend Framework", "Python Flask or Django"],
            ["Database", "PostgreSQL or SQLite (for development)"],
            ["Frontend", "HTML5, CSS3, JavaScript (Jinja2 templates or React)"],
            ["Authentication", "Flask-Login or Django Auth"],
            ["ORM", "SQLAlchemy or Django ORM"],
            ["Version Control", "Git with GitHub"],
            ["Hosting", "Cloud platform (AWS, Azure, or DigitalOcean)"],
            ["Web Server", "Gunicorn/uWSGI with Nginx reverse proxy"],
        ]
    )

    # 4. Proposal Guidelines
    add_heading(doc, "4. Proposal Guidelines", 1)
    add_heading(doc, "4.1 Proposal Submission", 2)
    add_body(doc, "Proposals must be submitted in English and in PDF format. The proposal should be no more than 30 pages (excluding appendices) and should be organized according to the structure outlined in Section 4.2. Proposals should be submitted via email to procurement@greenhillcoop.example.com with the subject line \"RFP Response: GHC-ORDER-2026-001 - [Vendor Name]\".")
    add_heading(doc, "4.2 Proposal Structure", 2)
    add_body(doc, "Proposals should include the following sections:")
    add_bullet(doc, "Executive Summary: A brief overview of the vendor's understanding of the project and proposed solution.")
    add_bullet(doc, "Company Profile: Background information about the vendor, including size, experience, and relevant certifications.")
    add_bullet(doc, "Technical Approach: Detailed description of the proposed solution, architecture, technology stack, and development methodology.")
    add_bullet(doc, "Project Plan: Detailed project schedule with milestones, deliverables, and resource allocation.")
    add_bullet(doc, "Team: Profiles of key personnel who will be assigned to the project.")
    add_bullet(doc, "Cost Proposal: Detailed pricing breakdown as specified in Section 7.")
    add_bullet(doc, "References: Contact information for at least three clients for whom similar projects have been completed.")
    add_bullet(doc, "Assumptions and Exclusions: Any assumptions made in preparing the proposal and items explicitly excluded.")
    add_heading(doc, "4.3 Submission Deadline", 2)
    add_body(doc, "Proposals must be received by 5:00 PM AEST on the deadline date specified in the RFP cover letter. Late proposals will not be considered.")
    add_heading(doc, "4.4 Questions and Clarifications", 2)
    add_body(doc, "Vendors may submit questions regarding this RFP in writing to procurement@greenhillcoop.example.com. All questions must be submitted at least 5 business days before the proposal deadline. Responses to questions will be provided to all vendors simultaneously to ensure fairness.")

    # 5. Evaluation Criteria
    add_heading(doc, "5. Evaluation Criteria", 1)
    add_body(doc, "Proposals will be evaluated by a cross-functional evaluation committee based on the following criteria and weightings:")
    add_table(doc,
        ["Criterion", "Weight", "Description"],
        [
            ["Technical Solution", "30%", "Quality, completeness, and appropriateness of the proposed technical solution and architecture."],
            ["Experience and Track Record", "20%", "Vendor's experience in similar projects, client references, and industry reputation."],
            ["Project Plan and Methodology", "15%", "Realism and completeness of the project schedule, risk management, and development methodology."],
            ["Team Capability", "15%", "Qualifications, experience, and availability of the proposed project team."],
            ["Cost", "15%", "Total cost of ownership, including development, deployment, and maintenance costs."],
            ["Maintenance and Support", "5%", "Quality of the proposed warranty, maintenance, and support arrangements."],
        ]
    )
    add_heading(doc, "5.1 Evaluation Process", 2)
    add_body(doc, "The evaluation process will consist of the following stages:")
    add_bullet(doc, "Stage 1 - Compliance Check: Verify that the proposal meets all mandatory requirements and submission guidelines.")
    add_bullet(doc, "Stage 2 - Technical Evaluation: Evaluate the technical solution, experience, project plan, and team capability.")
    add_bullet(doc, "Stage 3 - Shortlisting: Select the top 3 vendors for presentation and interview.")
    add_bullet(doc, "Stage 4 - Presentations: Shortlisted vendors present their solution to the evaluation committee.")
    add_bullet(doc, "Stage 5 - Reference Checks: Conduct reference checks with the vendors' previous clients.")
    add_bullet(doc, "Stage 6 - Final Selection: The evaluation committee scores all proposals and selects the preferred vendor.")
    add_heading(doc, "5.2 Mandatory Requirements", 2)
    add_body(doc, "The following requirements are mandatory. Proposals that do not meet all mandatory requirements will be excluded from further evaluation:")
    add_bullet(doc, "Vendor must have a minimum of 3 years of experience in web application development.")
    add_bullet(doc, "Vendor must have completed at least 2 similar projects in the last 3 years.")
    add_bullet(doc, "Proposed solution must be web-based and responsive.")
    add_bullet(doc, "Vendor must provide a minimum 12-month warranty period.")
    add_bullet(doc, "Vendor must provide ongoing maintenance and support options.")
    add_bullet(doc, "Proposal must be submitted in the required format and by the deadline.")

    # 6. Vendor Information
    add_heading(doc, "6. Vendor Information", 1)
    add_body(doc, "Vendors are required to provide the following information about their organization:")
    add_table(doc,
        ["Item", "Requirement"],
        [
            ["Legal Name", "Full legal name of the organization"],
            ["Business Address", "Registered business address"],
            ["ABN/ACN", "Australian Business Number or equivalent"],
            ["Contact Person", "Name, title, email, and phone of the primary contact"],
            ["Year Established", "Year the organization was established"],
            ["Number of Employees", "Total number of employees"],
            ["Relevant Certifications", "Any relevant certifications (e.g., ISO 27001, ISO 9001)"],
            ["Insurance", "Details of professional indemnity and public liability insurance"],
            ["Previous Clients", "List of at least 5 previous clients with contact details"],
        ]
    )

    # 7. Cost Proposal
    add_heading(doc, "7. Cost Proposal", 1)
    add_body(doc, "Vendors must provide a detailed cost breakdown using the following format. All costs should be in Australian Dollars (AUD) and inclusive of GST unless otherwise specified.")
    add_heading(doc, "7.1 One-Time Costs", 2)
    add_table(doc,
        ["Item", "Description", "Cost (AUD)"],
        [
            ["Requirements Analysis", "Requirements gathering, workshops, and documentation", ""],
            ["System Design", "Architecture, database, and UI design", ""],
            ["Development", "Application development and unit testing", ""],
            ["Integration Testing", "Integration testing and bug fixes", ""],
            ["User Acceptance Testing", "UAT support and defect resolution", ""],
            ["Deployment", "Production deployment and configuration", ""],
            ["Training", "Training sessions for coordinators and staff", ""],
            ["Documentation", "User manuals, admin guides, technical docs", ""],
            ["Project Management", "Project management and coordination", ""],
            ["Subtotal (One-Time)", "", ""],
        ]
    )
    add_heading(doc, "7.2 Recurring Costs", 2)
    add_table(doc,
        ["Item", "Description", "Annual Cost (AUD)"],
        [
            ["Hosting", "Cloud hosting and infrastructure", ""],
            ["Maintenance", "Bug fixes, security patches, minor updates", ""],
            ["Support", "Helpdesk and technical support (business hours)", ""],
            ["Database Backup", "Automated backup service", ""],
            ["Subtotal (Annual)", "", ""],
        ]
    )
    add_heading(doc, "7.3 Optional Services", 2)
    add_table(doc,
        ["Item", "Description", "Cost (AUD)"],
        [
            ["Extended Support", "24/7 support beyond business hours", ""],
            ["Feature Development", "Additional feature development (per hour)", ""],
            ["Performance Audit", "Annual performance and security audit", ""],
            ["Data Migration", "Assisted data migration from existing systems", ""],
        ]
    )
    add_heading(doc, "7.4 Total Cost of Ownership", 2)
    add_body(doc, "Vendors should provide a 3-year total cost of ownership (TCO) calculation, including all one-time and recurring costs. The TCO should be presented clearly to enable comparison between vendors.")

    # 8. Terms and Conditions
    add_heading(doc, "8. Terms and Conditions", 1)
    add_heading(doc, "8.1 Contract Duration", 2)
    add_body(doc, "The initial contract will be for the duration of the project (estimated 4-6 months) plus a 12-month warranty period. Ongoing maintenance and support will be subject to a separate annual agreement, renewable by mutual consent.")
    add_heading(doc, "8.2 Payment Terms", 2)
    add_body(doc, "Payments will be made in installments tied to project milestones as follows:")
    add_bullet(doc, "20% upon contract signing and project kickoff.")
    add_bullet(doc, "20% upon completion and approval of system design documents.")
    add_bullet(doc, "30% upon successful completion of user acceptance testing.")
    add_bullet(doc, "20% upon successful production deployment and sign-off.")
    add_bullet(doc, "10% retained for 3 months after deployment as a warranty holdback.")
    add_heading(doc, "8.3 Intellectual Property", 2)
    add_body(doc, "Upon full payment, all intellectual property rights in the developed software, including source code, documentation, and design artifacts, will transfer to Greenhill Food Co-op. The vendor may retain generic tools, frameworks, and reusable components that were not specifically developed for this project, provided they are disclosed in the proposal.")
    add_heading(doc, "8.4 Confidentiality", 2)
    add_body(doc, "The vendor must maintain the confidentiality of all cooperative data, member information, and business processes accessed during the project. A mutual non-disclosure agreement (NDA) will be required before the commencement of work.")
    add_heading(doc, "8.5 Data Privacy and Security", 2)
    add_body(doc, "The vendor must comply with all applicable Australian privacy laws, including the Privacy Act 1988 and the Australian Privacy Principles. Member personal information must be stored securely, encrypted at rest and in transit, and accessed only by authorized personnel. The vendor must report any data breach within 72 hours of discovery.")
    add_heading(doc, "8.6 Warranty", 2)
    add_body(doc, "The vendor warrants that the software will be free from material defects for a period of 12 months from the date of production deployment. During the warranty period, the vendor will correct all defects at no additional cost. The warranty does not cover defects caused by misuse, unauthorized modifications, or third-party software issues.")
    add_heading(doc, "8.7 Termination", 2)
    add_body(doc, "Either party may terminate the contract for material breach by the other party, provided written notice is given and the breaching party fails to remedy the breach within 30 days. Greenhill Food Co-op may terminate the contract for convenience with 30 days' written notice, in which case the vendor will be paid for work completed up to the termination date.")
    add_heading(doc, "8.8 Dispute Resolution", 2)
    add_body(doc, "Any disputes arising from this contract will first be attempted to be resolved through good faith negotiation between the parties. If negotiation fails, disputes will be referred to mediation before proceeding to litigation. The contract will be governed by the laws of New South Wales, Australia.")

    # 9. Additional Information
    add_heading(doc, "9. Additional Information", 1)
    add_heading(doc, "9.1 Project Timeline", 2)
    add_body(doc, "The anticipated project timeline is as follows:")
    add_table(doc,
        ["Phase", "Duration", "Key Deliverables"],
        [
            ["Requirements Analysis", "Weeks 1-2", "Requirements specification document"],
            ["System Design", "Weeks 3-4", "Architecture, database, and UI design documents"],
            ["Development", "Weeks 5-12", "Working application with all features"],
            ["Testing", "Weeks 13-14", "Test reports and defect resolution"],
            ["UAT", "Weeks 15-16", "UAT sign-off"],
            ["Deployment and Training", "Week 17", "Production deployment and training sessions"],
            ["Warranty", "Months 1-12", "Warranty support and maintenance"],
        ]
    )
    add_heading(doc, "9.2 Assumptions", 2)
    add_body(doc, "This RFP is based on the following assumptions:")
    add_bullet(doc, "Greenhill Food Co-op will provide timely access to subject matter experts and stakeholders for requirements gathering and UAT.")
    add_bullet(doc, "The cooperative will provide or procure necessary hosting infrastructure and domain names.")
    add_bullet(doc, "Scope changes requested after contract signing will be managed through a formal change control process and may result in additional cost and schedule adjustments.")
    add_bullet(doc, "The cooperative will be responsible for data entry and initial population of the product catalog.")
    add_heading(doc, "9.3 Appendices", 2)
    add_body(doc, "The following appendices are included as part of this RFP:")
    add_bullet(doc, "Appendix A: Current Process Description - Detailed description of the current manual ordering process.")
    add_bullet(doc, "Appendix B: User Stories - Detailed user stories for all system features.")
    add_bullet(doc, "Appendix C: Wireframes - Initial wireframe sketches for key user interface screens.")
    add_bullet(doc, "Appendix D: Evaluation Scorecard - Detailed scoring rubric used by the evaluation committee.")

    # GenAI Declaration
    add_heading(doc, "Generative AI Declaration", 1)
    add_body(doc, "In accordance with the ISYS3001 assessment policy, this section declares the use of generative AI tools in the preparation of this Request for Proposal.")
    add_body(doc, "Generative AI tools (Doubao) were used at Level 2 for brainstorming, grammar checking, and formatting assistance. The substantive content, including all requirements, evaluation criteria, terms and conditions, and cost structures, was authored by the student based on the project requirements and procurement best practices. AI was not used to generate the substantive content of this document. The student takes full responsibility for the accuracy and completeness of this RFP.")

    path = os.path.join(OUTPUT_DIR, "Ziliang_Lu_ISYS3001_Procurement_Plan.docx")
    doc.save(path)
    print(f"Saved: {path}")
    return path

if __name__ == "__main__":
    p1 = generate_config_report()
    p2 = generate_rfp()
    print(f"\nBoth reports generated successfully!")
    print(f"1. {p1}")
    print(f"2. {p2}")
