# LogPattern Analyzer

A bash tool for searching and filtering log files by pattern, date, and time range, with results exported to CSV and JSON in addition to plain text.

## Features
- Built-in pattern presets: errors/warnings, IP addresses, email addresses, usernames
- Custom regex patterns supported
- Optional date and time-range filtering
- Interactive menu mode or command-line arguments
- Outputs matches to a log file, CSV, and JSON, plus a level-count summary

## Usage

Interactive mode:
\`\`\`
./logpattern_analyzer.sh --menu
\`\`\`

Argument mode:
\`\`\`
./logpattern_analyzer.sh <pattern-type|regex> [date] [start_time] [end_time] [logfile]
\`\`\`

Example:
\`\`\`
./logpattern_analyzer.sh error 2024-01-15 10:00:00 12:00:00 auth.log
\`\`\`

## Pattern types
- \`error\` — matches error, warning, critical
- \`ip\` — matches IPv4 addresses
- \`email\` — matches email addresses
- \`user\` — matches "User <username>" patterns
- anything else is treated as a custom regex

## Output
- \`matches.log\` — numbered matching lines
- \`matches.csv\` — Line, Date, Time, Level, Message columns
- \`matches.json\` — same fields as structured JSON