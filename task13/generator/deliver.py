"""The two golden deliverables, built from the golden route's own table and figures: the feeder table
(vegetation_catchup_2027_feeders.csv, every feeder ranked) and the board note
(vegetation_catchup_2027_board_note.docx, with one chart). The note passes through the house container writer."""
import csv
import os

import common as C
import postprocess as PP

BLUE = '#2a6fb5'
GREY = '#b8bec6'
INK, INK2, GRID = '#111111', '#4d4d4d', '#e4e4e4'


def write_csv(F, R, path):
    T = R['T']
    trims = R['trims']
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['rank', 'feeder', 'weather_station', 'last_cycle_trim', 'tree_interruptions_2027_28_left_as_is',
                    'customers_per_tree_interruption', 'customer_interruptions_2027_28_left_as_is',
                    'customer_interruptions_2027_28_after_catchup', 'customer_interruptions_avoided', 'in_catchup'])
        for f in T.index:
            r = T.loc[f]
            w.writerow([int(r['rank']), f, R['station'][f], trims[f][-1].strftime('%Y-%m-%d'), '%.1f' % r['keep_n'],
                        int(round(r['cpe'])), int(round(r['keep_ci'])), int(round(r['cu_ci'])), int(round(r['avoided'])),
                        'Y' if f in F['six'] else 'N'])


def chart_png(F, R, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    T = R['T']
    vals = [float(T.loc[f, 'avoided']) for f in T.index]
    cols = [BLUE if f in F['six'] else GREY for f in T.index]
    fig, ax = plt.subplots(figsize=(6.6, 3.1), dpi=200)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    xs = range(len(vals))
    ax.bar(xs, vals, width=0.72, color=cols, zorder=3)
    for k, f in enumerate(T.index[:6]):
        ax.text(k, vals[k] + 35, f, ha='center', va='bottom', fontsize=5.6, color=INK, rotation=90)
    seventh = T.index[6]
    ax.text(6, vals[6] + 35, seventh, ha='center', va='bottom', fontsize=5.6, color=INK2, rotation=90)
    ax.set_xticks([])
    ax.set_xlim(-0.8, len(vals) - 0.2)
    ax.set_ylabel('Customer interruptions avoided', fontsize=8, color=INK2)
    ax.set_xlabel('The 48 feeders of the 11 kV network, ranked', fontsize=8, color=INK2)
    ax.set_ylim(0, max(vals) * 1.28)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: '{:,.0f}'.format(v)))
    ax.tick_params(axis='y', labelsize=7.5, colors=INK2, length=0)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#9a9a9a')
    ax.set_title('Six northern coastal feeders avoid %s customer interruptions in 2027-28'
                 % '{:,}'.format(F['avoided_total']), fontsize=8.6, color=INK, loc='left', pad=7)
    fig.tight_layout()
    fig.savefig(path, format='png', metadata={'Software': None})
    plt.close(fig)


def _cell(cell, text, bold=False, size=8.5, align=None):
    from docx.shared import Pt
    cell.text = ''
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if align is not None:
        p.alignment = align


def write_note(F, R, path, png):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Mm, Pt, RGBColor
    import officepdf as OP
    T = R['T']
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(21)
    sec.top_margin, sec.bottom_margin = Mm(17), Mm(16)
    st = doc.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(10)

    def para(text, bold=False, size=10, after=5, color=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.bold = bold
        r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return p
    for k, v in [('To', 'Board of Directors, Kotuku Networks Limited'),
                 ('From', '%s, General Manager Network' % C.PEOPLE['network_gm']),
                 ('Prepared by', '%s, Reliability Engineer' % C.PEOPLE['reliability_eng']),
                 ('Date', '19 November 2026'),
                 ('Subject', 'The six feeders for the 2027 vegetation catch-up (for approval)')]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run('%s:\t' % k)
        r1.bold = True
        r1.font.size = Pt(9.5)
        r2 = p.add_run(v)
        r2.font.size = Pt(9.5)
    para('', after=2)
    six = F['six']
    para('Recommendation: put %s, %s, %s, %s, %s and %s into the 2027 catch-up' % tuple(six), bold=True, size=13, after=6)
    q = F['quarters']
    para('On these six northern coastal feeders the catch-up avoids about %s sustained customer interruptions caused by '
         'vegetation in 2027-28, the most it can avoid on any six of the network’s 48 feeders. That is %.2f of network '
         'SAIFI on the %s ICPs connected at 31 October 2026. The next-best feeder, %s, would avoid %s. The saving is '
         'heaviest in the winter quarter: %s in April to June 2027, %s in July to September, %s in October to '
         'December and %s in January to March 2028. In nine years out of ten the six avoid between %s and %s, '
         'depending on the year’s storms.'
         % ('{:,}'.format(F['avoided_total']), F['saifi_avoided'], '{:,}'.format(F['icps_latest']), F['seventh'],
            '{:,}'.format(F['seventh_avoided']), '{:,}'.format(q[0]), '{:,}'.format(q[1]), '{:,}'.format(q[2]),
            '{:,}'.format(q[3]), '{:,}'.format(F['range90'][0]), '{:,}'.format(F['range90'][1])), after=5)
    para('Why these six', bold=True, size=10.5, after=3)
    para('Their corridors have gone longest since a cycle trim: each was last trimmed between October 2019 and May '
         '2020, and through 2027-28 each will be seven and a half to eight years from its trim. Across the network a '
         'corridor’s vegetation interruptions, for the same wind, rise about %.1f per cent for every year since its last '
         'trim, so these six carry the most growth that a trim takes away. Left as they stand they would have the six '
         'largest counts of vegetation interruptions in an ordinary year; after the catch-up most of that falls away.'
         % F['growth_per_year_pct'], after=5)
    para('Why not the feeders with the most interruptions now', bold=True, size=10.5, after=3)
    stn = F['stations']
    d6 = F['default_six']
    para('The feeders with the most vegetation customer interruptions in the three years to October 2026 are %s, '
         'mostly the plantation feeders of the southern hills. Two things make that list the wrong one for this '
         'decision. First, those three years were unusual weather: Titi Saddle and Kowhai Ridge recorded about %d and %d '
         'hours a year with gusts of 60 km/h or more against their usual %d and %d, while Paua Bay recorded %d against '
         'its usual %d. The mean wind at every station moved by only a few per cent, so the difference sits in the '
         'damaging gusts, and the recent counts overstate the southern feeders and understate the northern ones. '
         'Second, the plantation corridors were cut in the second half of 2025 on their three-year cycle, and most of '
         'their interruptions come from the density of the corridor itself, which a catch-up does not change.'
         % (', '.join(d6[:-1]) + ' and ' + d6[-1], stn['TSD']['recent'], stn['KWR']['recent'], stn['TSD']['normal'],
            stn['KWR']['normal'], stn['PBA']['recent'], stn['PBA']['normal']), after=5)
    para('How the figures were made', bold=True, size=10.5, after=3)
    para('Each feeder’s vegetation interruptions from April 2022 were read month by month against the gust load at '
         'its nearest weather station (each hour’s gust above 40 km/h, squared and added up), as a rate for the '
         'corridor straight after a cycle trim that grows with the years since the trim. Of the measures of wind we '
         'tried, the gust load fits the record best. 2027-28 is then taken at each station’s average year from 2006 to '
         '2025, with the corridor left as it stands and with the catch-up finished on 31 March 2027, and counted in '
         'customer interruptions at the feeder’s own customers per vegetation interruption. Other measures of the wind '
         '(hours of gusts from 45 to 70 km/h, the gust excess over 35 or 45 km/h), other base years and other forms for '
         'the growth give the same six, with totals from %s to %s. The range is the spread of the six’s '
         'saving across the weather of every complete regulatory year in the station record, 2006-07 to 2025-26, the 5th to the '
         '95th percentile, with the corridors and their growth held as fitted.'
         % ('{:,}'.format(F['family_total_range'][0]), '{:,}'.format(F['family_total_range'][1])), after=6)
    tbl = doc.add_table(rows=1, cols=5)
    tbl.style = 'Table Grid'
    hdr = ['Feeder', 'Weather station', 'Customer interruptions, left as is', 'After the catch-up', 'Avoided']
    for j, h in enumerate(hdr):
        _cell(tbl.rows[0].cells[j], h, bold=True)
    for f in six:
        r = tbl.add_row().cells
        row = T.loc[f]
        vals = [f, R['station'][f], '{:,}'.format(int(round(row['keep_ci']))), '{:,}'.format(int(round(row['cu_ci']))),
                '{:,}'.format(int(round(row['avoided'])))]
        for j, v in enumerate(vals):
            _cell(r[j], v, align=None if j < 2 else WD_ALIGN_PARAGRAPH.RIGHT)
    r = tbl.add_row().cells
    tot_keep, tot_cu = F['keep_six_total'], F['cu_six_total']
    for j, v in enumerate(['The six', '', '{:,}'.format(tot_keep), '{:,}'.format(tot_cu), '{:,}'.format(F['avoided_total'])]):
        _cell(r[j], v, bold=True, align=None if j < 2 else WD_ALIGN_PARAGRAPH.RIGHT)
    para('Sustained unplanned interruptions coded to vegetation, counted under the Reliability Reporting Standard, '
         'excluding major event days. Figures are rounded after they are added.', size=8, after=6, color='4D4D4D')
    doc.add_picture(png, width=Mm(166))
    para('Every feeder’s figures are in vegetation_catchup_2027_feeders.csv.¹', size=8, after=8, color='4D4D4D')
    para('¹ The major event days since April 2022 were the %d snow days on the southern hills; no day of strong wind '
         'reached a boundary value.' % F['med_days'], size=7.5, after=0, color='4D4D4D')
    fp = sec.footer.paragraphs[0]
    rr = fp.add_run('Kotuku Networks. Board paper, November 2026. In confidence.   Page ')
    rr.font.size = Pt(7.5)
    OP._page_field(fp)
    doc.save(path)
    created, modified = C.GOLD_STAMP['note']
    PP.normalize_docx(path, C.PEOPLE['network_gm'], C.PEOPLE['reliability_eng'], C.utc_z(created), C.utc_z(modified),
                      5, 186, 6173, title='2027 vegetation catch-up: the six feeders', company=C.ORG)


def build(F, R, golden_dir):
    import shutil
    import tempfile
    if os.path.exists(golden_dir):
        shutil.rmtree(golden_dir)
    os.makedirs(golden_dir)
    write_csv(F, R, os.path.join(golden_dir, C.DELIVERABLES[0]))
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, 'chart.png')
    chart_png(F, R, png)
    write_note(F, R, os.path.join(golden_dir, C.DELIVERABLES[1]), png)
    shutil.rmtree(tmp)
    PP.own_mtimes(golden_dir, {C.DELIVERABLES[0]: C.local(C.GOLD_STAMP['csv'][1])})
