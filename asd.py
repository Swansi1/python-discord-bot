asd = '''<HTML>

<BODY>
	<CENTER>
		<H2>SZTE teremkereső Google térképpel</H2>
	</Center>
	<br>


	<FORM METHOD="post">
		<TABLE align=center border=0 cellpadding="5" cellspaceing="5">
			<TR>
				<TD>Keresendő</TD>
				<TD><INPUT TYPE="text" NAME="search" SIZE=20 MAXLENGTH=100 VALUE="BO-211"></TD>
			</TR>
			<tr>
				<td colspan=2 align="right">
					<INPUT TYPE="submit" NAME="submit" VALUE="Keres">
					<!--
    &nbsp;&nbsp;&nbsp;
    <INPUT TYPE="submit" NAME="submit" VALUE="KILÉP">
    -->
				</td>
			</tr>
		</TABLE>
	</FORM>
	<TABLE BORDER=1 cellpadding=2>
		<TR>
			<TD><b>Kar</b></TD>
			<TD><b>Épület</b></TD>
			<TD><b>Emelet</b></TD>
			<TD><b>Terem</b></TD>
			<TD><b>Típus</b></TD>
			<TD><b>Férőhely</b></TD>
			<TD><b>Cím és térképlink</b></TD>
		</TR>
		<TR>
			<TD>TTIK</TD>
			<TD>Bolyai épület</TD>
			<TD>Bolyai épület - 2. emelet</TD>
			<TD>BO-211-3 - Szőkefalvi-Nagy terem (II. emelet)</TD>
			<TD>Előadó</TD>
			<TD>72</TD>
			<TD><a href="." target="_blank">Szeged, Aradi
					vértanúk tere 1.</a></TD>
		</TR>
	</TABLE>

</BODY>

</HTML>'''

try:
    google_maps_pattern = asd.split("https://www.google.com/maps/search/")[1].split('"')[0]
except IndexError:
    google_maps_pattern = ""
    print("szopika")
print(google_maps_pattern)
