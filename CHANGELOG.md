# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* User profiles now have a `role` field for managing permissions in the upcoming GraphQL API
* Added components for upcoming GraphQL API that are only available with _local.yml_ for testing in development environments
  * New Docker container for Hasura GraphQL engine
  * Work-in-progress Hasura metadata for the GraphQL API
  * New `HASURA_ACTION_SECRET` envionment variable to templates
  * New utilities for generating and managing JSON Web Tokens for the GraphQL API

# Removed

* Removed "WHOIS Privacy" colum on domain list page to make room for more petinent information

### Fixed

* Bumped `djangorestframework-api-key` to v2.2.0 to fix REST API key creation (closes #197)
* Overrode Django's ``get_full_name()`` method used for the admin site so the user's proper full name is displayed in history logs

### Changed

* Disabled `L10N` by default in favor of using `DATE_FORMAT` for managing the server's preferred date format (closes #193)
* Updated env templates with a `DATE_FORMAT` configuration for managing your preferred format
  * See updated installation documentation on ghostwriter.wiki
* User profiles now only show the user's role, groups, and Ghostwriter user status to the profile owner
* Updated nginx.conf to align it with Mozilla's recommendations for nginx v1.21.1 and OpenSSL 1.1.1l
  * See config: [https://ssl-config.mozilla.org/#server=nginx&version=1.21.1&config=intermediate&openssl=1.1.1l&ocsp=false&guideline=5.6](https://ssl-config.mozilla.org/#server=nginx&version=1.21.1&config=intermediate&openssl=1.1.1l&ocsp=false&guideline=5.6)
* Toast messages for errors are no longer sticky so they do not have to be manually dismissed when covering UI elements
* Updated singleton models for Django 4.0 support
* Domain list table now shows an "Expiry" column and "Categories" column now parses the new ``categorization`` JSON field data
* Domain list filtering now includes a "Filter Expired" toggle that on by default
  * Filters out domains with expiration dates in the past and `auto_renew` set to `False` even if status is set to "Available"

## [2.2.3] - 2022-02-16

### Added

* Expanded user profiles for project management and planning
  * Now visible to all users under /users/
  * Include timezone and phone number fields -Users can now edit their profiles to update their preferred name, phone, timezone, and email address

### Fixed

* Fixed display of minutes for project working hours
* Fixed "incomplete file" issue when attempting to download a report template
* Fixed report archiving failing to write zip file
* Fixed toast messages not showing up when swapping report templates
* Fixed sidebar tab appearing below delete confirmations
* Fixed cloud server forms requiring users to fill in all auxiliary IP addresses
* Fixed project serialization issue that prevented project data from loading automatically for domain and server checkout forms
* Fixed active project filtering for the list in the sidebar so it will no longer contain some projects marked as completed
* Fixed a rare reporting error that could occur if the WYSIWYG editor created a block of nested HTML tags with no content
* Fixed ignore tags not working for Digital Ocean assets
* Fixed an error caused by cascading deletes when deleting a report under some circumstances
* Fixed template linter not recognizing phone numbers for project team members as valid (Fixes #190)
* Fixed a rare reporting issue related to nested lists that could occur if a nested list existed below an otherwise blank list item

### Changed

* Updated project list filtering
  * Added client name as a filter field
  * Changed default display filter to only show active projects
  * Adjusted project status filter to have three options: all projects, active projects, and completed projects
* Updated dashboard and calendar to show past and current events for browsing history within the calendar
  * Past events marked as completed will appear dimed with a strikethrough and `: Complete` added to the end
* Upgraded dependencies to their latest versions (where possible)
  * Django v3.1.13 -> v3.2.11
  * Did not upgrade `docxtpl`
    * Awaiting to see how the developer wants to proceed with [issue #114](https://github.com/elapouya/python-docx-template/issues/414)
    * Not upgrading from 0.12 to the latest 0.15.2 has no effect on Ghostwriter at this time
* Collapsed the `Domain` model's various categorization fields into a single `categorization` field with PostgreSQL's `JSONField` type
  * An important milestone/change for the upcoming GraphQL API
  * Categorization is no longer limited to specific vendors
  * Going forward, the field can be manually updated with valid JSON
  * Ghostwriter will look for JSON formatted as a series of keys and values: `{"COMPANY": "CATEGORY", "COMPANY": "CATEGORY",}`
* Converted the `ReportTemplate` model's `lint_result` field to a PostgreSQL `JSONField`
  * An important milestone/change for the upcoming GraphQL API
  * This change increases reliability and performance by removing any need to transform a string representation back into a `dict`
  * Little to no impact on users but templates may need to be linted again after the upgrade
  * If a template is affected, the status will change to "Unknown" with a single warning note: "Need to re-run linting following your Ghostwriter upgrade"
* Converted the `Domain` model's `dns_record` field to a PostgreSQL `JSONField` and renamed it to `dns` for simplicity
  * An important milestone/change for the upcoming GraphQL API
  * This change increases reliability and performance by removing any need to transform a string representation back into a `dict`
  * This field was always intended to be edited only by the server, so this change should not require any actions before or after upgrading
  * If an existing record's DNS data cannot be converted to JSON it will be cleared and user's can re-run the DNS update task
* Added a "sticky" sidebar tracker to user sessions so the sidebar will stay open or closed between visits and page changes
* Removed the legacy `health_dns` field from the `Domain` model
  * This field was part of the original Shepherd project and was an interesting experiment in using passive DNS monitoring to try to determine if a domain was "burned"
  * It became mostly irrelevant when services that supported this feature (e.g., eSentire's Cymon) were retired
* Changed some code that will be deprecated in future versions of Django v4.x and Python Faker
* Made it possible to sort the report template list
  * Sorting on this table is reversed so clicking "Status" once will sort templates with passing linter checks first
* Updated the admin panel to make it easier to manage domains for those who prefer the admin panel
* Projects now sort in reverse so the most recent projects appear first
* Updated the report selection section of the sidebar to make it easier to switch reports when working on multiple and navigate to your current report
* The logging API key message now includes the project ID to make it easier to set up a tool like mythic\_sync
* Removed the "Upload Evidence" button from editors where it does not apply (e.g., in the Finding Library outside of a report) (Fixes #185)
* Updated the Namecheap sync task to use paging so Namecheap libraries with more than 100 domains can be fully synced (Fixes #188)
* Dashboard once again has a "Project Assignments" card to make it easier to see and click projects
  * The calendar remains on the dashboard and is still clickable, but some people found it less intuitive as a shortcut
* Some general code clean-up for maintainability

### Security

* Updated Django to v3.2.11 as v3.1 is no longer supported and considered "insecure" going forward
* Fixed unauthenticated access to domain and server library exports
* Updated TinyMCE to v5.10.1 to address several moderate security issues with <5.10

## [2.2.3-rc2] - 2022-02-09

### Fixed

* Fixed "incomplete file" issue when attempting to download a report template
* Fixed report archiving failing to write zip file
* Fixed toast messages not showing up when swapping report templates
* Fixed sidebar tab appearing below delete confirmations

### Changed

* Upgraded dependencies to their latest versions (where possible)
  * Django v3.1.13 -> v3.2.11
  * Did not upgrade `docxtpl`&#x20;
    * Awaiting to see how the developer wants to proceed with [issue #114](https://github.com/elapouya/python-docx-template/issues/414)
    * Not upgrading from 0.12 to the latest 0.15.2 has no effect on Ghostwriter at this time
* Collapsed the `Domain` model's various categorization fields into a single `categorization` field with PostgreSQL's `JSONField` type
  * An important milestone/change for the upcoming GraphQL API
  * Categorization is no longer limited to specific vendors
  * Going forward, the field can be manually updated with valid JSON
  * Ghostwriter will look for JSON formatted as a series of keys and values: `{"COMPANY": "CATEGORY", "COMPANY": "CATEGORY",}`
* Converted the `ReportTemplate` model's `lint_result` field to a PostgreSQL `JSONField`
  * An important milestone/change for the upcoming GraphQL API
  * This change increases reliability and performance by removing any need to transform a string representation back into a `dict`
  * Little to no impact on users but templates may need to be linted again after the upgrade
  * If a template is affected, the status will change to "Unknown" with a single warning note: "Need to re-run linting following your Ghostwriter upgrade"
* Converted the `Domain` model's `dns_record` field to a PostgreSQL `JSONField` and renamed it to `dns` for simplicity
  * An important milestone/change for the upcoming GraphQL API
  * This change increases reliability and performance by removing any need to transform a string representation back into a `dict`
  * This field was always intended to be edited only by the server, so this change should not require any actions before or after upgrading
  * If an existing record's DNS data cannot be converted to JSON it will be cleared and user's can re-run the DNS update task
* Added a "sticky" sidebar tracker to user sessions so the sidebar will stay open or closed between visits and page changes
* Removed the legacy `health_dns` field from the `Domain` model
  * This field was part of the original Shepherd project and was an interesting experiment in using passive DNS monitoring to try to determine if a domain was "burned"
  * It became mostly irrelevant when services that supported this feature (e.g., eSentire's Cymon) were retired
* Changed some code that will be deprecated in future versions of Django v4.x and Python Faker
* Made it possible to sort the report template list
  * Sorting on this table is reversed so clicking "Status" once will sort templates with passing linter checks first
* Updated the admin panel to make it easier to manage domains for those who prefer the admin panel
* Some general code clean-up for maintainability

### Security

* Updated Django to v3.2.11 as v3.1 is no longer supported and considered "insecure" going forward
* Fixed unauthenticated access to domain and server library exports

## [2.2.3-rc1] - 2022-01-28

### Added

* Expanded user profiles for project management and planning
  * Now visible to all users under /users/
  * Include timezone and phone number fields -Users can now edit their profiles to update their preferred name, phone, timezone, and email address

### Fixed

* Fixed cloud server forms requiring users to fill in all auxiliary IP addresses
* Fixed project serialization issue that prevented project data from loading automatically for domain and server checkout forms
* Fixed active project filtering for the list in the sidebar so it will no longer contain some projects marked as completed
* Fixed a rare reporting error that could occur if the WYSIWYG editor created a block of nested HTML tags with no content
* Fixed ignore tags not working for Digital Ocean assets
* Fixed an error caused by cascading deletes when deleting a report under some circumstances
* Fixed template linter not recognizing phone numbers for project team members as valid (Fixes #190)
* Fixed a rare reporting issue related to nested lists that could occur if a nested list existed below an otherwise blank list item

### Changed

* Projects now sort in reverse so the most recent projects appear first
* Updated the report selection section of the sidebar to make it easier to switch reports when working on multiple and navigate to your current report
* The logging API key message now includes the project ID to make it easier to set up a tool like mythic\_sync
* Removed the "Upload Evidence" button from editors where it does not apply (e.g., in the Finding Library outside of a report) (Fixes #185)
* Updated the Namecheap sync task to use paging so Namecheap libraries with more than 100 domains can be fully synced (Fixes #188)
* Dashboard once again has a "Project Assignments" card to make it easier to see and click projects
  * The calendar remains on the dashboard and is still clickable, but some people found it less intuitive as a shortcut
* Some general clean-up of CSS

### Security

* Updated TinyMCE to v5.10.1 to address several moderate security issues with <5.10

## [2.2.2] - 2021-10-22

### Added

* Added new filters for report templates
  * `add_days`: Add some number of business days to a date
  * `format_datetime`: Change the format of the provided datetime string
* The cloud monitoring task can now collect information about AWS Lightsail instances and S3 buckets
* A new "Notification Delay" setting is available under the Cloud Configurations
  * This setting delays cloud infrastructure teardown notifications by X days
  * Useful if you want to run the cloud monitor task more frequently and not get teardown reminders for some period of time after a project ends
* Projects now have fields for  timezone, start time, and end time to track working hours
* Client contacts now have a timezone field
* You can now save up to three additional IP addresses for cloud servers (they are stored in an array for easy iteration)

### Fixed

* Fixed the sorting of the domain age column in the domain table
* Fixed issue with the JavaScript for deleting entries in a formset selecting other checkboxes
* Fixed `WhoisStatus` model's `count` property
* Fixed error handling that could suppress report generation error messages when generating all reports
* Fixed error that could lead to WebSocket disconnections and errors when editing the timestamp values of a log entry
* Fixed a typo in the emoji used by the default Slack message for an untracked server
* Fixed a logic issue that could result in an "ignore tag" being missed when reporting on cloud infrastructure

### Changed

* Adjusted the report data to replace a blank short name with the client's full name (rather than a blank space in a report)
* Moved some form validation logic to Django Signals in preparation for the API
* Added a custom "division by zero" error message for times when a Jinja2 template attempts to divide a value (e.g., total num of completed objectives) that is zero without first checking the value
* Bumped Toastr message opacity to `.9` (up from `.8`) to improve readability
* Bumped 50 character limit on certain `OplogEntry` values to 255 (the standard for other models)
* Condensed Docker image layers and disabled caching for `pip` and `apk` to reduce image sizes by about 0.2 to 0.3GB
* Optimized and improved code quality throughout the project based on recommendations from Code Factor ([https://www.codefactor.io/repository/github/ghostmanager/ghostwriter](https://www.codefactor.io/repository/github/ghostmanager/ghostwriter))
* Added Signals to release a checked-out server or domain if the current checkout is deleted (so it is released immediately rather than waiting for a scheduled task to run)
* When updating a project's dates, Ghostwriter will no longer update the dates on domain and server checkouts if the checkout has already expired
* If an in-use domain is flagged as "burned" by the health check task, a notification will now be sent to the project's Slack channel if a Slack channel is configured
* All core libraries have been bumped up to their latest versions and Django has been upgraded to v3.1 from v3.0

### Security

* Upgraded the Django image to Alpine v3.14 to address potential security vulnerabilities in the base image
* Upgraded Postgres image to Postgres v11.12 to address potential security vulnerabilities in previously used version/base image
* Pinned nginx image to v1.12.1 for security and stability
* Upgraded TinyMCE to v5.8.2 to address potential XSS discovered in older TinyMCE versions

## [2.2.2-rc3] - 2021-09-27

### Added

* Projects now have fields for  timezone, start time, and end time to track working hours
* User profiles and client contacts now have a timezone field
* You can now save up to three additional IP addresses for cloud servers \(they are stored in an array for easy iteration\)

## [2.2.2-rc2] - 2021-09-22

### Added

* The cloud monitoring task can now collect information about AWS Lightsail instances and S3 buckets
* A new "Notification Delay" setting is available under the Cloud Configurations
  * This setting delays cloud infrastructure teardown notifications by X days
  * Useful if you want to run the cloud monitor task more frequently and not get teardown reminders for some period of time after a project ends

### Changed

* Added Signals to release a checked-out server or domain if the current checkout is deleted \(so it is released immediately rather than waiting for a scheduled task to run\)
* If an in-use domain is flagged as "burned" by the health check task, a notification will now be sent to the project's Slack channel if a Slack channel is configured

## [2.2.2-rc1] - 2021-09-15

### Fixed

* Fixed issue with the JavaScript for deleting entries in a formset selecting other checkboxes
* Fixed `WhoisStatus` model's `count` property
* Fixed error handling that could suppress report generation error messages when generating all reports
* Fixed error that could lead to WebSocket disconnections and errors when editing the timestamp values of a log entry
* Fixed a typo in the emoji used by the default Slack message for an untracked server
* Fixed a logic issue that could result in an "ignore tag" being missed when reporting on cloud infrastructure

### Changed

* Adjusted the report data to replace a blank short name with the client's full name \(rather than a blank space in a report\)
* Moved some form validation logic to Django Signals in preparation for the API
* Added a custom "division by zero" error message for times when a Jinja2 template attempts to divide a value \(e.g., total num of completed objectives\) that is zero without first checking the value
* Bumped Toastr message opacity to `.9` \(up from `.8`\) to improve readability
* Bumped 50 character limit on certain `OplogEntry` values to 255 \(the standard for other models\)
* Condensed Docker image layers and disabled caching for `pip` and `apk` to reduce image sizes by about 0.2 to 0.3GB
* Optimized and improved code quality throughout the project based on recommendations from Code Factor \([https://www.codefactor.io/repository/github/ghostmanager/ghostwriter](https://www.codefactor.io/repository/github/ghostmanager/ghostwriter)\)

### Security

* Upgraded TinyMCE to v5.8.2 to address potential XSS discovered in older TinyMCE versions
* Upgraded the Django image to Alpine v3.14 to address potential security vulnerabilities in the base image
* Upgraded Postgres image to Postgres v11.12 to address potential security vulnerabilities in previously used version/base image
* Pinned nginx image to v1.12.1 for security and stability

## [2.2.1] - 2021-05-28

### Added

* Every page now includes a footer at the bottom of the content that displays the version number of the  Ghostwriter server.

### Fixed

* Findings with no assigned editors will no longer prevent report generation.

### Changed

* Findings in a report now have an `ordering` value that represents their position in the report \(starting at zero with the top finding in the most severe category\).
* Headings throughout the interface are no longer all caps by default \(this could negatively affect readability\).
* Some form elements will no longer appear far apart when the interface is fullscreen on a very high-resolution or wide-screen display.

## [2.2.0] - 2021-05-10

### Added

* Added new `filter_type` filter to report templates \(submitted by @5il with PR \#152\).
* Introduced the new `ReportData` serializer. This is nearly invisible to users but is a huge efficiency and performance upgrade for the back-end. Changes to project data models will now automatically appear in the raw JSON reports and be accessible within DOCX reports.
* The new serializer has modified some of the Jinja2 template expressions. View a JSON report to see everything available. For example, instead of writing `{{ project_codename }}`, you will access this project value with `{{ project.codename }}`.
* Ghostwriter now handles dates differently to better support all international date formats. Dates displayed in the interface and dates within reports \(e.g., `report_date`\) will match the date locale set in your server settings \(`en-us` by default\).

### Fixed

* Updated broken POC contact edit URL on the client details page
* Project assignment dates will no longer be improperly adjusted on updates
* Template linter context now has entries for new RichText objects
* Adjusted HTML parser to account for the possibility for empty fields following an update from one of the older versions of Ghostwriter  \(submitted by @Abstract-9 with PR \#158\)
* Adjusted Dockerfile files to fix potential filesystem issues with the latest Alpine Linux image \(submitted by @studebacon with PR \#143\).
* Added a missing field in the Report Template admin panel
* "Add to Report" on the finding details page now works
* Updated delete actions for operation logs to avoid anerror that could prevent the deletion of entries when deleting an entire log
* Domain age calculations are now accurate
* An invalid value for domain purchase date no longer causes a server error during validation
* Constrained `Twisted` library to v20.3.0 to fix a potential issue that could come up with Django Channels
  * [https://github.com/django/channels/issues/1639](https://github.com/django/channels/issues/1639)
* Improved the reporting engine to handle even the wildest nested styling

### Changed

* Adjusted finding severity lists to sort by the severity's weight instead of alphabetically.
* Re-enabled evidence uploads in all WYSIWYG editors \(it was previously excluded from certain finding fields\).
* Adjusted sidebar organization to improve visibility of a few sections that could be difficult to locate.
* Updated BootStrap and FontAwesome CSS versions.
* Updated all Python libraries to their latest versions.
* Animated the hamburger menus for fun.
* Switched ASGI servers \(from Daphne server to Uvicorn\) for WebSockets and better performance.
* Updated the sample _template.docx_ to act as a walkthrough for the new report data and changes in Jinja2 expressions.

## [2.2.0-rc2] - 2022-04-13

### Added

* Introduced the new `ReportData` serializer. This is nearly invisible to users but is a huge efficiency and performance upgrade for the back-end. Changes to project data models will now automatically appear in the raw JSON reports and be accessible within DOCX reports.
* The new serializer has modified some of the Jinja2 template expressions. View a JSON report to see everything available. For example, instead of writing `{{ project_codename }}`, you will access this project value with `{{ project.codename }}`.
* Ghostwriter now handles dates differently to better support all international date formats. Dates displayed in the interface and dates within reports \(e.g., `report_date`\) will match the date locale set in your server settings \(`en-us` by default\).

### Fixed

* Added a missing field in the Report Template admin panel.
* "Add to Report" on the finding details page now works.
* Updated delete actions for operation logs to avoid an error that could prevent the deletion of entries when deleting an entire log.
* Domain age calculations are now accurate.
* An invalid value for domain purchase date no longer causes a server error during validation.
* Constrained `Twisted` library to v20.3.0 to fix a potential issue that could come up with Django Channels
  * [https://github.com/django/channels/issues/1639](https://github.com/django/channels/issues/1639)
* Improved the reporting engine to handle even the wildest nested styling.

### Changed

* Adjusted finding severity lists to sort by the severity's weight instead of alphabetically.
* Re-enabled evidence uploads in all WYSIWYG editors \(it was previously excluded from certain finding fields\).
* Adjusted sidebar organization to improve visibility of a few sections that could be difficult to locate.
* Updated BootStrap and FontAwesome CSS versions.
* Updated all Python libraries to their latest versions.
* Animated the hamburger menus for fun.
* Switched ASGI servers \(from Daphne server to Uvicorn\) for WebSockets and better performance.
* Updated the sample _template.docx_ to act as a walkthrough for the new report data and changes in Jinja2 expressions.

## [2.1.1] - 2021-03-05

### Fixed

* Fixed server error when trying to create a new project with an assignment or objective
* Fixed edge case that could cause a new task below an objective to be duplicated
* Fixed edge case that would flag a project target form as invalid if it had a note and did not also have both an IP address and hostname
* Fixed toggle arrow working in reverse when a user marks an objective complete while tasks are expanded

### Changed

* Made it so objective completion percentage updates when a new task is added or deleted
* Made it possible to use `@` targets for Slack channels instead of only `#` channels
* The `uploaded_by` values are now set on report templates on the server-side

## [2.1] - 2021-03-03

### Added

* Implemented project scope tracking (closes #59)
    * Enabled tracking of one or more scope lists flagged as allowed/disallowed or requiring caution
* Implemented project target tracking
    * Enabled tracking of specific hosts with notes
* Committed redesigned project dashboards
    * Notable changes and adjustments:
        * Added a project calendar to track assignments, objectives, tasks, and project dates
        * Added new objective tracker with task management, prioritization, and sorting
* Implemented a new server search in the side bar (under _Servers_) that searches all static servers, cloud servers in projects, and alternate addresses tied to servers
* Added template linting checks for additional styles that may not be present in a report (closes #139)
* Added Clipboard.js to support better, more flexible "click to copy to clipboard" in the UI
* Added several new Jinja2 expressions, statements, and filters for Word DOCX reports
    * Added `project_codename` and `client_codename` (closes #138)
    * Added expressions and filters for new objectives, targets, and scope lists
    * See wiki documentation
* Implemented initial support for WebSocket channels for reports

### Changed

* Tagged release, v2.1
    * Release will require database migrations
    * New features will require reloading the `seed_data` file
        * e.g., `docker-compose -f local.yml run --rm django /seed_data`
* Improved page loading with certain large forms
    * WYSIWYG editor is now loaded much more selectively
    * Extra forms are no longer created by default when _editing_ a project or client
        * Extra forms can still be added as needed
        * Extra forms still load automatically when _creating_ a new project or client
* Improved performance of operation log entry views with pagination
    * Very large logs could push browsers to their limits

### Fixed

* Fixed downloads of document names that included periods and commas (closes #149)
* Fixed evidence filenames with all uppercase extensions not appearing in reports (closes #74)
* Fixed a recursive HTML/JavaScript escape in log entries (closes #133)
* Fixed incorrect link in the menu for a point of contact under a client (closed #141 and #141)
* Fixed `docker-compose` errors related to latest verison of the `crytpography` library (closes #147)
* Fixed possible issue with assigning a name to an AWS asset in the cloud monitor task
* Closed loophole that could allow a non-unique domain name

### Security

* Updated TinyMCE WYSIWYG editor and related JavaScript to v5.7.0
    * Resolved potential Cross-Site Scripting vulnerability discovered in previous version

## [2.0.2] - 2021-01-15

### Changed

* Added error handling for cases where an image file has a corrupted file header and can't be recognized for inserting into Word
* Moved 99% of icons and style elements to the _styles.css_ file

### Fixed

* Fixed notifications going to the global Slack channel when project channels were available
* Fixed uppercase file extensions blocking evidence files from appearing on pages
* Fixed rare `style` exception with specific nested HTML elements

## [2.0.2] - 2020-12-18

### Changed

* Updated styles and forms to make it clear what is placeholder text
* Reverted the new finding form to a one-page form–i.e., no tabbed sections–to make it easier to use
* Broke-up stylesheets for easier management of global variables

### Fixed

* Fixed error in cloud monitor notification messages that caused messages to contain the same external IP addresses for all VPS instances
* Fixed bug that caused delete actions on cloud server entries to not be committed
* Fixed `ref` tags in findings that were ingored if they followed a `ref` tag with a different target
* Fixed PowerPoint "Conclusion" slide's title
* Fixed filtering for report template selection dropdowns that caused both document types to appear in all dropdown menus

## [2.0.1] - 2020-12-03

### Added

* Added project objectives to the report template variables
    * New template keywords: `objectives` (List), `objectives_total` (Int), `objectives_complete` (Int)

### Changed

* Modified project "complete" toggle and instructions for clarity
* Set all domain names to lowercase and strip any spaces before creating or updating
    * Addressed cases where a user error could create a duplicate entry
* Clicking prepended text (e.g., filter icon) on filter form fields will now submit the filter

### Fixed

* Fixed error that could cause Oplog entries to not display
* Oplog entries list now shows loading messages and properly displays "no entries" messages
* Fixed incorrect filenames for CSV exports of Oplogs

## [2.0.0] - 2020-11-20

### Added

* Initial commit of CommandCenter application and related configuration options
    * VirusTotal Configuration
    * Global Report Configuration
    * Slack Configuration
    * Company information
    * Namecheap Configuration
* Initial support for adding users to groups for Role-Based Access Controls
* Automated Activity Logging (Oplog application) moved out of beta
* Implemented initial "overwatch" notifications
    * Domain check-out: alert if domain will expire soon and is not set to auto-renew
    * Domain check-out: alert if domain is marked as burned
    * Domain check-out: alert if domain has been previously used with selected client

### Changed

* Upgraded to Django 3 and updated all dependencies
* Updated user interface elements
    * New tabbed dashboards for clients, projects, and domains
    * New inline forms for creating and managing clients and projects and related items
    * New sidebar menu to improve legibility
    * Migrated buttons and background tasks to WebSockets and AJAX for a more seamless experience
* Initial release of refactored reporting engine (closes #89)
    * New drag-and-drop report management interface
    * Added many more options to the WYSIWYG editor's formatting menus
    * Initial support for rich text objects for Word documents
    * Added new `filter_severity` filter for Word templates
* Initial support for report template and management (closes #28 and #90)
    * Upload report template files for Word and PowerPoint
    * New template linter to check and verify templates
* Removed web scraping from domain health checks (closed #50 and #84)
    * Checks now use VirusTotal and link to the results
* Numerous bug fixes and enhancements to address reported issues (closes #54, #55, #69, #92, #93, and #98)

### Security

* Resolved potential stored cross-site scripting in operational logs
* Resolved unvalidated evidence file uploads and new note creation
    * Associated user account is now set server-side
* Resolved issues with WebSocket authentication
* Locked-down evidence uploads to close potential loopholes
    * Evidence form now only allows specific filetypes: md, txt, log, jpg, jpeg, png
    * Requesting an evidence file requires an active user session