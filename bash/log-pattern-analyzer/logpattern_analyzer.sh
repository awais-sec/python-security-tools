#!/bin/bash

# ========== CONFIG ==========
DEFAULT_LOGFILE="sample.log"
OUTPUTFILE="matches.log"
CSVFILE="matches.csv"
JSONFILE="matches.json"

# ========== COLORS ==========
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m"

# ========== PATTERN TYPES ==========
function get_pattern_by_type() {
  case "$1" in
    error) echo "error|warning|critical" ;;
    ip) echo "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" ;;
    email) echo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" ;;
    user) echo "User [a-zA-Z0-9_]+" ;;
    *) echo "$1" ;;
  esac
}

# ========== INTERACTIVE MENU ==========
if [[ "$1" == "--menu" ]]; then
  echo -e "${CYAN}Interactive Mode:${NC}"
  echo "Select pattern to search:"
  echo "1. Error/Warning"
  echo "2. IP Addresses"
  echo "3. Email Addresses"
  echo "4. Usernames"
  echo "5. Custom"
  read -p "Choose [1-5]: " choice

  case $choice in
    1) PATTERN_TYPE="error" ;;
    2) PATTERN_TYPE="ip" ;;
    3) PATTERN_TYPE="email" ;;
    4) PATTERN_TYPE="user" ;;
    5) read -p "Enter custom pattern (regex/string): " PATTERN_TYPE ;;
    *) echo "Invalid choice"; exit 1 ;;
  esac

  PATTERN=$(get_pattern_by_type "$PATTERN_TYPE")
  read -p "Enter date filter (YYYY-MM-DD or blank): " DATE_FILTER
  read -p "Start time (HH:MM:SS or blank): " START_TIME
  read -p "End time (HH:MM:SS or blank): " END_TIME
  read -p "Enter log file (or blank for default): " LOGFILE
  # fall back to the default logfile if left blank, same as argument mode
  LOGFILE="${LOGFILE:-$DEFAULT_LOGFILE}"
else
  # ARGUMENT MODE
  PATTERN_TYPE="$1"
  DATE_FILTER="$2"
  START_TIME="$3"
  END_TIME="$4"
  LOGFILE="${5:-$DEFAULT_LOGFILE}"
  PATTERN=$(get_pattern_by_type "$PATTERN_TYPE")
fi

# ========== VALIDATION ==========
if [[ -z "$PATTERN" ]]; then
  echo -e "${RED}Usage:${NC} $0 <pattern-type|regex> [date] [start_time] [end_time] [logfile]"
  echo "       OR: $0 --menu"
  exit 1
fi

echo -e "${GREEN}Pattern:${NC} $PATTERN"
[[ $DATE_FILTER ]] && echo -e "${GREEN}Date:${NC} $DATE_FILTER"
[[ $START_TIME && $END_TIME ]] && echo -e "${GREEN}Time range:${NC} $START_TIME to $END_TIME"
echo -e "${GREEN}File:${NC} $LOGFILE"

# ========== FILTER ==========
MATCHES=$(grep -iE "$PATTERN" "$LOGFILE")

if [[ $DATE_FILTER ]]; then
  MATCHES=$(echo "$MATCHES" | grep "$DATE_FILTER")
fi

if [[ $START_TIME && $END_TIME ]]; then
  MATCHES=$(echo "$MATCHES" | awk -v start="$START_TIME" -v end="$END_TIME" '
    {
      time = substr($2, 1, 8)
      if (time >= start && time <= end) print
    }
  ')
fi

# ========== OUTPUT ==========
# space separator here instead of a colon, since the log lines already
# contain colons in the timestamp and that was throwing off the awk
# splitting further down
echo "$MATCHES" | nl -w1 -s' ' > "$OUTPUTFILE"
echo -e "\n${CYAN}Matched lines:${NC}"
cat "$OUTPUTFILE"

# ========== CSV EXPORT ==========
# line format after numbering: <num> <date> <time> <LEVEL> <message...>
# splitting on whitespace keeps date/time whole and lines up level and
# message correctly, unlike the old colon+space split
echo "Line,Date,Time,Level,Message" > "$CSVFILE"
awk 'NF >= 4 {
  msg = $5
  for (i = 6; i <= NF; i++) msg = msg " " $i
  gsub(/"/, "\"\"", msg)
  print $1","$2","$3","$4",\"" msg "\""
}' "$OUTPUTFILE" >> "$CSVFILE"

# ========== JSON EXPORT ==========
echo "[" > "$JSONFILE"
awk 'NF >= 4 {
  msg = $5
  for (i = 6; i <= NF; i++) msg = msg " " $i
  gsub(/"/, "\\\"", msg)
  printf "  {\"line\": %s, \"date\": \"%s\", \"time\": \"%s\", \"level\": \"%s\", \"message\": \"%s\"},\n",
  $1, $2, $3, $4, msg
}' "$OUTPUTFILE" | sed '$ s/,$//' >> "$JSONFILE"
echo "]" >> "$JSONFILE"

# ========== SUMMARY ==========
echo -e "\n${YELLOW}Summary:${NC}"
MATCH_COUNT=$(wc -l < "$OUTPUTFILE")
echo "Total matches: $MATCH_COUNT"

for LEVEL in INFO WARNING ERROR DEBUG CRITICAL
do
  COUNT=$(grep -i "$LEVEL" "$OUTPUTFILE" | wc -l)
  [[ $COUNT -gt 0 ]] && echo -e "${GREEN}$LEVEL:${NC} $COUNT"
done

echo -e "\nFiles saved:"
echo " - $OUTPUTFILE"
echo " - $CSVFILE"
echo " - $JSONFILE"
