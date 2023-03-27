from bs4 import BeautifulSoup
from dataclasses import dataclass
import csv

hitting_standard = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">GP</th><th class="statCell header">PA</th><th class="statCell header">AB</th><th class="statCell header">H</th><th class="statCell header">1B</th><th class="statCell header">2B</th><th class="statCell header">3B</th><th class="statCell header">HR</th><th class="statCell header">RBI</th><th class="statCell header">R</th><th class="statCell header">HBP</th><th class="statCell header">ROE</th><th class="statCell header">FC</th><th class="statCell header">CI</th><th class="statCell header">BB</th><th class="statCell header">SO</th><th class="statCell header">AVG</th><th class="statCell header">OBP</th><th class="statCell header">SLG</th><th class="statCell header">OPS</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">40</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000004">Aidan Cann</a></td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1.000</td><td class="statCell">1.000</td><td class="statCell">1.000</td><td class="statCell">2.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">2</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000d">Benjamin Schattman</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">.250</td><td class="statCell">.250</td><td class="statCell">.250</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">2</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">1.000</td><td class="statCell">1.500</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">11</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000009">Joe Goncalves</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">1.000</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">17</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000012">Luca Vasiliu</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">8</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6406a568e64e4e00f5000001">Michael Leonard</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.250</td><td class="statCell">.250</td><td class="statCell">.250</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">15</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000002">Nick Aderhold</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">1.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">14</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000014">Nick Wong</a></td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">3</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.667</td><td class="statCell">.667</td><td class="statCell">.667</td><td class="statCell">1.333</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">7</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000010">Quincy Steidle</a></td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">2</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.500</td><td class="statCell">.333</td><td class="statCell">.500</td><td class="statCell">.833</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">6</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a0952900062c">Rashad</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">1.000</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">3</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000f">Sammy Spingola</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">42</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000006">Shawn Charles</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">1.000</td><td class="statCell">1.500</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">1</td><td class="statCell">33</td><td class="statCell">32</td><td class="statCell">13</td><td class="statCell">10</td><td class="statCell">2</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">10</td><td class="statCell">.406</td><td class="statCell">.394</td><td class="statCell">.531</td><td class="statCell">.925</td></tr></tfoot>
    </table>'''

hitting_psp = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">GP</th><th class="statCell header">PA</th><th class="statCell header">AB</th><th class="statCell header">PA/BB</th><th class="statCell header">BB/K</th><th class="statCell header">C%</th><th class="statCell header">K-L</th><th class="statCell header">SB</th><th class="statCell header">CS</th><th class="statCell header">SB%</th><th class="statCell header">PIK</th><th class="statCell header">GIDP</th><th class="statCell header">GITP</th><th class="statCell header">XBH</th><th class="statCell header">TB</th><th class="statCell header">AB/HR</th><th class="statCell header">BA/RISP</th><th class="statCell header">SLG</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">40</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000004">Aidan Cann</a></td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">1.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">2</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000d">Benjamin Schattman</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.250</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">11</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000009">Joe Goncalves</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">17</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000012">Luca Vasiliu</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">8</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6406a568e64e4e00f5000001">Michael Leonard</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.250</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">15</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000002">Nick Aderhold</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">14</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000014">Nick Wong</a></td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">3</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">.667</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">7</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000010">Quincy Steidle</a></td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">6</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a0952900062c">Rashad</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">3</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000f">Sammy Spingola</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">42</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000006">Shawn Charles</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">1</td><td class="statCell">33</td><td class="statCell">32</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.688</td><td class="statCell">8</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">3</td><td class="statCell">17</td><td class="statCell">.000</td><td class="statCell">.308</td><td class="statCell">.531</td></tr></tfoot>
    </table>'''

hitting_qabs = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">GP</th><th class="statCell header">PA</th><th class="statCell header">AB</th><th class="statCell header">PA/BB</th><th class="statCell header">BB/K</th><th class="statCell header">C%</th><th class="statCell header">K-L</th><th class="statCell header">SB</th><th class="statCell header">CS</th><th class="statCell header">SB%</th><th class="statCell header">PIK</th><th class="statCell header">GIDP</th><th class="statCell header">GITP</th><th class="statCell header">XBH</th><th class="statCell header">TB</th><th class="statCell header">AB/HR</th><th class="statCell header">BA/RISP</th><th class="statCell header">SLG</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">40</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000004">Aidan Cann</a></td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">1.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">2</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000d">Benjamin Schattman</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.250</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">11</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000009">Joe Goncalves</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">17</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000012">Luca Vasiliu</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">8</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6406a568e64e4e00f5000001">Michael Leonard</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.250</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">15</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000002">Nick Aderhold</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">14</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000014">Nick Wong</a></td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">3</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">.667</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">7</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000010">Quincy Steidle</a></td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">6</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a0952900062c">Rashad</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">3</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000f">Sammy Spingola</a></td><td class="statCell">1</td><td class="statCell">2</td><td class="statCell">2</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.500</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">42</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000006">Shawn Charles</a></td><td class="statCell">1</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">4</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">1.000</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">1</td><td class="statCell">33</td><td class="statCell">32</td><td class="statCell">.000</td><td class="statCell">.000</td><td class="statCell">.688</td><td class="statCell">8</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">3</td><td class="statCell">17</td><td class="statCell">.000</td><td class="statCell">.308</td><td class="statCell">.531</td></tr></tfoot>
    </table>'''

pitching_standard = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">IP</th><th class="statCell header">GP</th><th class="statCell header">GS</th><th class="statCell header">W</th><th class="statCell header">L</th><th class="statCell header">SV</th><th class="statCell header">SVO</th><th class="statCell header">BS</th><th class="statCell header">SV%</th><th class="statCell header">H</th><th class="statCell header">R</th><th class="statCell header">ER</th><th class="statCell header">BB</th><th class="statCell header">SO</th><th class="statCell header">HBP</th><th class="statCell header">ERA</th><th class="statCell header" title="Walks plus hits per innings pitched">WHIP</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">3.0</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">4</td><td class="statCell">4</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">5</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">1.667</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">12</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000008">Michael D’Amore</a></td><td class="statCell">1.1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">1.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">16</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a08d040005f1">Tung</a></td><td class="statCell">2.2</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">6</td><td class="statCell">6</td><td class="statCell">6</td><td class="statCell">4</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">20.250</td><td class="statCell">3.750</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">7.0</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">12</td><td class="statCell">10</td><td class="statCell">6</td><td class="statCell">5</td><td class="statCell">9</td><td class="statCell">0</td><td class="statCell">7.714</td><td class="statCell">2.429</td></tr></tfoot>
    </table>'''

pitching_command = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">IP</th><th class="statCell header">BF</th><th class="statCell header">TS</th><th class="statCell header">S%</th><th class="statCell header">FPS</th><th class="statCell header">FPS%</th><th class="statCell header">FPSO%</th><th class="statCell header">FPSW%</th><th class="statCell header">FPSH%</th><th class="statCell header">BB/INN</th><th class="statCell header">0BBINN</th><th class="statCell header">BBS</th><th class="statCell header">LOBB</th><th class="statCell header">LOBBS</th><th class="statCell header">WP</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">3.0</td><td class="statCell">18</td><td class="statCell">43</td><td class="statCell">.632</td><td class="statCell">13</td><td class="statCell">.722</td><td class="statCell">.769</td><td class="statCell">.000</td><td class="statCell">.231</td><td class="statCell">.333</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">12</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000008">Michael D’Amore</a></td><td class="statCell">1.1</td><td class="statCell">6</td><td class="statCell">17</td><td class="statCell">.708</td><td class="statCell">5</td><td class="statCell">.833</td><td class="statCell">.600</td><td class="statCell">.000</td><td class="statCell">.400</td><td class="statCell">.000</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">16</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a08d040005f1">Tung</a></td><td class="statCell">2.2</td><td class="statCell">16</td><td class="statCell">29</td><td class="statCell">.492</td><td class="statCell">6</td><td class="statCell">.375</td><td class="statCell">.667</td><td class="statCell">.167</td><td class="statCell">.167</td><td class="statCell">1.500</td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">7.0</td><td class="statCell">40</td><td class="statCell">89</td><td class="statCell">.589</td><td class="statCell">24</td><td class="statCell">.600</td><td class="statCell">.708</td><td class="statCell">.042</td><td class="statCell">.250</td><td class="statCell">.714</td><td class="statCell">4</td><td class="statCell">3</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td></tr></tfoot>
    </table>'''

pitching_batter = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">IP</th><th class="statCell header">BF</th><th class="statCell header">ABA</th><th class="statCell header">#P</th><th class="statCell header">SM</th><th class="statCell header">SM%</th><th class="statCell header">SO</th><th class="statCell header">K/G</th><th class="statCell header">K/BF</th><th class="statCell header">K/BB</th><th class="statCell header">WEAK%</th><th class="statCell header">HHB%</th><th class="statCell header">GB%</th><th class="statCell header">FLB%</th><th class="statCell header">GO</th><th class="statCell header">FO</th><th class="statCell header">GO/FO</th><th class="statCell header">BAA</th><th class="statCell header">HR</th><th class="statCell header">BABIP</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">3.0</td><td class="statCell">18</td><td class="statCell">16</td><td class="statCell">68</td><td class="statCell">6</td><td class="statCell">.088</td><td class="statCell">5</td><td class="statCell">15.000</td><td class="statCell">.278</td><td class="statCell">5.000</td><td class="statCell">1.000</td><td class="statCell">.000</td><td class="statCell">.667</td><td class="statCell">.333</td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">.333</td><td class="statCell">.250</td><td class="statCell">0</td><td class="statCell">.333</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">12</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000008">Michael D’Amore</a></td><td class="statCell">1.1</td><td class="statCell">6</td><td class="statCell">6</td><td class="statCell">24</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">2</td><td class="statCell">13.500</td><td class="statCell">.333</td><td class="statCell">.000</td><td class="statCell">1.000</td><td class="statCell">.000</td><td class="statCell">.750</td><td class="statCell">.250</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">.000</td><td class="statCell">.333</td><td class="statCell">0</td><td class="statCell">.500</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">16</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a08d040005f1">Tung</a></td><td class="statCell">2.2</td><td class="statCell">16</td><td class="statCell">12</td><td class="statCell">59</td><td class="statCell">5</td><td class="statCell">.085</td><td class="statCell">2</td><td class="statCell">6.750</td><td class="statCell">.125</td><td class="statCell">.500</td><td class="statCell">.900</td><td class="statCell">.100</td><td class="statCell">.200</td><td class="statCell">.800</td><td class="statCell">1</td><td class="statCell">3</td><td class="statCell">.333</td><td class="statCell">.500</td><td class="statCell">0</td><td class="statCell">.600</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">7.0</td><td class="statCell">40</td><td class="statCell">34</td><td class="statCell">151</td><td class="statCell">11</td><td class="statCell">.073</td><td class="statCell">9</td><td class="statCell">11.571</td><td class="statCell">.225</td><td class="statCell">1.800</td><td class="statCell">.962</td><td class="statCell">.038</td><td class="statCell">.500</td><td class="statCell">.500</td><td class="statCell">4</td><td class="statCell">6</td><td class="statCell">.667</td><td class="statCell">.353</td><td class="statCell">0</td><td class="statCell">.462</td></tr></tfoot>
    </table>'''

pitching_runs = \
'''<table class="gcTable statTable withGridLines withOutline withHoverHighlighting">
        <thead><tr><th class="jerseyNumberCell header">#</th><th class="playerNameCell invertLinkUnderline strong header headerSortDown">Roster</th><th class="statCell header">IP</th><th class="statCell header">LOB</th><th class="statCell header">BK</th><th class="statCell header">PIK</th><th class="statCell header">SB</th><th class="statCell header">CS</th><th class="statCell header">SB%</th></tr></thead>
        <tbody><tr class="whiteRow odd"><td class="jerseyNumberCell">23</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c00000e">Drew Seidman</a></td><td class="statCell">3.0</td><td class="statCell">5</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">.000</td></tr><tr class="greyRow even"><td class="jerseyNumberCell">12</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-640424614cea87ae8c000008">Michael D’Amore</a></td><td class="statCell">1.1</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">0</td><td class="statCell">1.000</td></tr><tr class="whiteRow odd"><td class="jerseyNumberCell">16</td><td class="playerNameCell invertLinkUnderline strong"><a href="/player-6420a568e676a08d040005f1">Tung</a></td><td class="statCell">2.2</td><td class="statCell">2</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">.000</td></tr></tbody>
        <tfoot><tr><td class="footerTitleCell" colspan="2">Totals</td><td class="statCell">7.0</td><td class="statCell">9</td><td class="statCell">0</td><td class="statCell">0</td><td class="statCell">1</td><td class="statCell">1</td><td class="statCell">.500</td></tr></tfoot>
    </table>'''

# format is: AB, R, H, 2B, 3B, HR, RBI, BB, IBB, SO, SB, CS, SAC-F, SAC-B, HBP
@dataclass
class Hitting:
    ab: int
    r: int
    h: int
    doubles: int
    triples: int
    hr: str
    rbi: int
    bb: int
    ibb: int
    so: int
    sb: int
    cs: int
    sac_f: int
    sac_b: int
    hbp: int


@dataclass
class Pitching:
    started: int
    w: int
    l: int
    cg: str
    sho: str
    sv: int
    svo: int
    ip: str
    h: int
    r: int
    er: int
    hr: int
    hbp: int
    bb: int
    ibb: int
    so: int
    bk: int
    wp: int
    pk: int


# Map name -> stats
HITTING_STATS = dict()
PITCHING_STATS = dict()

def format_name(name: str):
    if ' ' not in name:
        return name
    split = name.index(' ')
    return f'{name[split+1:]}, {name[:split]}'


def parse_hitting(hitting_standard, hitting_psp, hitting_qabs):
    parse_hitting_standard(hitting_standard)
    parse_hitting_psp(hitting_psp)
    parse_hitting_qabs(hitting_qabs)


def parse_pitching(pitching_standard, pitching_command, pitching_batter, pitching_runs):
    parse_pitching_standard(pitching_standard)
    parse_pitching_command(pitching_command)
    parse_pitching_batter(pitching_batter)
    parse_pitching_runs(pitching_runs)


# parse "Standard" stats in GameChanger
def parse_hitting_standard(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows) - 1):
        details = rows[i].find_all('td')
        if len(details) < 18:
            continue

        person = format_name(details[1].text)

        ab = details[4].text
        runs = details[11].text
        hits = details[5].text
        doubles = details[7].text
        triples = details[8].text
        hr = details[9].text
        rbi = details[10].text
        bb = details[16].text
        ibb = 0 # gamechanger doesn't have this
        so = details[17].text
        hbp = details[12].text

        hitting = Hitting(ab, runs, hits, doubles, triples, hr, rbi, bb, ibb, so, 0, 0, 0, 0, hbp)
        HITTING_STATS[person] = hitting


# Parse "Patience, Speed & Power" from GameChanger
def parse_hitting_psp(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows) - 1):
        details = rows[i].find_all('td')
        if len(details) < 18:
            continue

        person = format_name(details[1].text)
        if person not in HITTING_STATS:
            print(f'Warning: hitting stats stats for {person} not entered yet. Skipping...')
            continue

        sb = details[9].text
        cs = details[10].text

        HITTING_STATS[person].sb = sb
        HITTING_STATS[person].cs = cs


def parse_hitting_qabs(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows) - 1):
        details = rows[i].find_all('td')
        if len(details) < 18:
            continue

        person = format_name(details[1].text)
        if person not in HITTING_STATS:
            print(f'Warning: hitting stats stats for {person} not entered yet. Skipping...')
            continue

        sac_b = details[13].text
        sac_f = details[14].text

        HITTING_STATS[person].sac_b = sac_b
        HITTING_STATS[person].sac_f = sac_f


# Parse "Standard" pitching statistics
def parse_pitching_standard(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows)-1):
        details = rows[i].find_all('td')

        if len(details) < 17:
            continue

        person = format_name(details[1].text)

        started = details[4].text
        w = details[5].text
        l = details[6].text
        cg = 'N/A'
        shutout = 'N/A'
        sv = details[7].text
        svo = details[8].text
        ip = details[2].text
        h = details[11].text
        r = details[12].text
        er = details[13].text
        hr = 0 # in batter results
        hbp = details[16].text
        bb = details[14].text
        ibb = 0 # not in GameChanger
        so = details[15].text
        bk = 0 # in runs & running game
        wp = 0 # in command
        pk = 0 # in runs & running game

        pitching = Pitching(started, w, l, cg, shutout, sv, svo, ip, h, r, er, hr, hbp, bb, ibb, so, bk, wp, pk)
        PITCHING_STATS[person] = pitching


def parse_pitching_command(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows)-1):
        details = rows[i].find_all('td')

        if len(details) < 17:
            continue

        person = format_name(details[1].text)
        if person not in PITCHING_STATS:
            print(f'Warning: pitching stats stats for {person} not entered yet. Skipping...')
            continue

        wp = details[16].text

        PITCHING_STATS[person].wp = wp


def parse_pitching_batter(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows)-1):
        details = rows[i].find_all('td')

        if len(details) < 17:
            continue

        person = format_name(details[1].text)
        if person not in PITCHING_STATS:
            print(f'Warning: pitching stats stats for {person} not entered yet. Skipping...')
            continue

        hr = details[20].text

        PITCHING_STATS[person].hr = hr
        


def parse_pitching_runs(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'gcTable'})
    rows = table.find_all('tr')
    for i in range(len(rows) - 1):
        details = rows[i].find_all('td')

        if len(details) < 9:
            continue

        person = format_name(details[1].text)
        if person not in PITCHING_STATS:
            print(f'Warning: pitching stats stats for {person} not entered yet. Skipping...')
            continue

        bk = details[4].text
        pk = details[5].text
        PITCHING_STATS[person].bk = bk
        PITCHING_STATS[person].pk = pk


with open('hitting_stats.csv', mode='w', newline='') as file:
    parse_hitting(hitting_standard, hitting_psp, hitting_qabs)

    writer = csv.writer(file)
    writer.writerow(['Name', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'SAC_F', 'SAC_B', 'HBP'])

    hitters = list(HITTING_STATS.keys())
    hitters.sort()

    for person in hitters:
        hit = HITTING_STATS[person]
        writer.writerow([person, 
                         hit.ab, 
                         hit.r, 
                         hit.h, 
                         hit.doubles, 
                         hit.triples, 
                         hit.hr, 
                         hit.rbi, 
                         hit.bb,
                         hit.ibb,
                         hit.so,
                         hit.sb,
                         hit.cs,
                         hit.sac_f,
                         hit.sac_b,
                         hit.hbp])
        

with open('pitching_stats.csv', mode='w', newline='') as file:
    parse_pitching(pitching_standard, pitching_command, pitching_batter, pitching_runs)

    writer = csv.writer(file)
    writer.writerow(['Name', 'Started', 'W', 'L', 'CG', 'SHO', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'HBP', 'BB', 'IBB', 'SO', 'BK', 'WP', 'PK'])
    
    pitchers = list(PITCHING_STATS.keys())
    pitchers.sort()

    for person in pitchers:
        pitch = PITCHING_STATS[person]
        writer.writerow([person,
                         pitch.started,
                         pitch.w,
                         pitch.l,
                         pitch.cg,
                         pitch.sho,
                         pitch.sv,
                         pitch.svo, 
                         pitch.ip,
                         pitch.h,
                         pitch.r, 
                         pitch.er, 
                         pitch.hr, 
                         pitch.hbp, 
                         pitch.bb, 
                         pitch.ibb, 
                         pitch.so, 
                         pitch.bk, 
                         pitch.wp, 
                         pitch.pk])
        
                         
 