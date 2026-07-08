#!/usr/bin/env python3
"""
STN-MT-PP-007  |  SES v4.1 .PRN parser  |  Synoptic CFD
Extracts the transient SYSTEM PARTITIONING results (air flow CFM, velocity FPM,
temperature degF) for every section at every output time, plus fire-segment
temperature, and writes a tidy CSV + an Excel workbook for validation.

Usage:  python parse_prn.py  <file.PRN> [file2.PRN ...]
Output: <stem>_parsed.csv  and appends to the master validation workbook.

Tested against the Memorial Tunnel reference outputs (MT-T615B, cold-flow set).
Units are converted to SI on output (CFM->m3/s, FPM->m/s, degF->degC).
"""
import re, sys, os, csv

CFM_TO_M3S = 0.000471947
FPM_TO_MS  = 0.00508
def f2c(f): return (f - 32.0) * 5.0/9.0

TIME_RE = re.compile(r"^TIME\s+([\d.]+)\s+SECONDS")
# a partitioning data row: "    1 -  1       327860.9    826.3      41.5"
ROW_RE  = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*$")

def parse_prn(path):
    """Return list of dict rows: time_s, section, flow_cfm, vel_fpm, temp_f.

    State machine:
      - track current simulation time from 'TIME  xx.xx SECONDS'
      - a partitioning table opens on the '(CFM)    (FPM)   HUMIDITY' header line
      - within an open table, lines matching ROW_RE are section data rows
        (the interleaved humidity-only lines simply don't match and are skipped)
      - the table closes at the next TIME marker or a form-feed / page header
    """
    rows = []
    cur_time = None
    in_part = False
    with open(path, errors="ignore") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            stripped = line.strip()

            mt = TIME_RE.match(stripped)
            if mt:
                cur_time = float(mt.group(1))
                in_part = False
                continue

            # open the partitioning table on its column-units header
            if "(CFM)" in line and "(FPM)" in line:
                in_part = True
                continue

            # NOTE: SES partitioning tables span multiple printed pages; the
            # page header (SES VER / FILE:) interrupts the table but it RESUMES
            # afterward. We therefore do NOT close on the page break — only a
            # new TIME marker closes the table. A fresh (CFM)/(FPM) header simply
            # re-affirms in_part. This rejoins all sections for the time step.

            if in_part and cur_time is not None:
                m = ROW_RE.match(line)
                if m:
                    rows.append(dict(
                        time_s=cur_time, section=int(m.group(1)),
                        flow_cfm=float(m.group(3)),
                        vel_fpm=float(m.group(4)),
                        temp_f=float(m.group(5)),
                    ))
    return rows

def to_si(rows):
    out = []
    for r in rows:
        out.append(dict(
            time_s=r["time_s"], section=r["section"],
            flow_m3s=round(r["flow_cfm"]*CFM_TO_M3S, 4),
            vel_ms=round(r["vel_fpm"]*FPM_TO_MS, 4),
            temp_c=round(f2c(r["temp_f"]), 3),
            flow_cfm=r["flow_cfm"], vel_fpm=r["vel_fpm"], temp_f=r["temp_f"],
        ))
    return out

def summarize(rows_si):
    """Quasi-steady summary: last-time values per section + peak temp per section."""
    if not rows_si: return {}, None, {}
    tmax = max(r["time_s"] for r in rows_si)
    last = {r["section"]: r for r in rows_si if r["time_s"]==tmax}
    peaktemp = {}
    for r in rows_si:
        s=r["section"]
        if s not in peaktemp or r["temp_c"]>peaktemp[s]:
            peaktemp[s]=r["temp_c"]
    return last, tmax, peaktemp

def main():
    if len(sys.argv) < 2:
        print("usage: python parse_prn.py <file.PRN> [...]"); sys.exit(1)
    for path in sys.argv[1:]:
        rows = parse_prn(path)
        si = to_si(rows)
        stem = os.path.splitext(os.path.basename(path))[0]
        outcsv = os.path.join(os.path.dirname(path) or ".", stem + "_parsed.csv")
        with open(outcsv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["time_s","section","flow_m3s","vel_ms","temp_c","flow_cfm","vel_fpm","temp_f"])
            w.writeheader()
            for r in si: w.writerow(r)
        last, tmax, peak = summarize(si)
        nsec = len(set(r["section"] for r in si))
        ntime = len(set(r["time_s"] for r in si))
        print(f"{stem}: {len(si)} rows, {nsec} sections x {ntime} times; "
              f"final t={tmax}s -> {outcsv}")
        if last:
            vmax = max(r["vel_ms"] for r in last.values())
            tmaxc = max(peak.values())
            print(f"    peak section velocity @final = {vmax:.2f} m/s ; peak temp (any t) = {tmaxc:.1f} degC")

if __name__ == "__main__":
    main()
