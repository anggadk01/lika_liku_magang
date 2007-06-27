<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">

	<xsl:import href="../../custom/corporate_defaults.xsl"/>
	<xsl:import href="../../base/report/rml_template.xsl"/>
	
	<xsl:template match="/">
		<xsl:call-template name="rml"/>
	</xsl:template>

	<!-- frames (optional template - override corporate defaults) -->

	<xsl:template name="first_page_frames">
<!--	
		<frame id="smalltext" x1="14.5cm" y1="26cm" width="6cm" height="3cm"/>
-->		
		<frame id="address" x1="11cm" y1="21.5cm" width="6cm" height="4cm"/>
		<frame id="main" x1="1cm" y1="3.5cm" width="19.0cm" height="17.5cm"/>
	</xsl:template>
	
	<!-- report specific "graphics" -->
	
	<xsl:template name="first_page_graphics_report">
		<setFont name="Helvetica" size="16"/>
		<drawCentredString x="105mm" y="28cm" t="1">PACKINGLIST</drawCentredString>
	</xsl:template>
	
	<!-- stylesheet -->

	<xsl:template name="stylesheet">
		<blockTableStyle id="infos">
			 <blockFont name="Helvetica-Bold" size="10" start="0,0" stop="-1,0"/>
			 <blockBackground colorName="grey" start="0,0" stop="-1,0"/>
			 <blockTextColor colorName="white" start="0,0" stop="-1,0"/>
			 <lineStyle kind="GRID" colorName="black"/>
		</blockTableStyle>
		<blockTableStyle id="products">
			 <blockBackground colorName="lightgrey" start="0,0" stop="-1,0"/>
			 <blockFont name="Helvetica-Bold" size="10" start="0,0" stop="-1,0"/>
			 <lineStyle kind="LINEBELOW" colorName="black" start="0,0" stop="-1,0"/>
			 <blockValign value="TOP"/>
			 <blockAlignment value="RIGHT" start="3,0" stop="3,-1"/>
			 <blockAlignment value="RIGHT" start="6,0" stop="6,-1"/>
		</blockTableStyle>
		<paraStyle name="address-title" fontName="Helvetica-Bold" fontSize="8" alignment="left"/>
		<paraStyle name="address" fontName="Helvetica" fontSize="8" alignment="left" leftIndent="1cm"/>
		<paraStyle name="prod" fontName="Helvetica" fontSize="10" alignment="left"/>
		<paraStyle name="prod-right" fontName="Helvetica" fontSize="10" alignment="right"/>
	</xsl:template>
	
	<xsl:template name="story">
		<xsl:apply-templates select="pickinglist"/>
	</xsl:template>
	
	<xsl:template match="pickinglist">
		<xsl:apply-templates select="picking"/>
	</xsl:template>
	
	<xsl:template match="picking">
		<xsl:apply-templates select="header"/>
		<xsl:apply-templates select="lines"/>
	</xsl:template>
	
	<xsl:template match="header">
		<!-- start of smalltext frame -->
<!--
		<para t="1">
			Here is the picking list of this lot. Generated by Tiny ERP.
		</para>
-->		
		<!-- end of smalltext frame -->
<!--		
		<nextFrame/>
-->		
		<!-- start of address frame -->
		
		<para style="address-title" t="1">
			Shipping Address:
		</para>
	
		<xsl:apply-templates select="corporation" mode="shipping"/>
		<xsl:apply-templates select="address" mode="shipping"/>
	
		<!-- end of address frame -->
	
		<nextFrame/>
	
		<!-- start of products frame -->
	
		<para>
			<b t="1">Recipient</b>: <xsl:apply-templates select="address" mode="header"/> 
		</para>
		<para t="1">
			Concerns: <xsl:value-of select="picking-name"/>
		</para>
	
		<spacer length="1cm" width="1mm"/>
	
		<blockTable colWidths="4cm,4cm,6cm,4cm" style="infos">
		<tr>
			<td t="1">Customer ref.</td>
			<td t="1">Shipping ref.</td>
			<td t="1">Packing Date</td>
			<td t="1">Shipping Date</td>
		</tr><tr>
			<td><para><xsl:value-of select="corporation/id"/></para></td>
			<td><para><xsl:value-of select="picking-id"/></para></td>
			<td><para><xsl:value-of select="picking-date"/></para></td>
			<td><para><xsl:value-of select="expedition-date"/></para></td>
		</tr>
		</blockTable>
	</xsl:template>
	
	<xsl:template match="corporation" mode="shipping">
		<para style="address">
			<xsl:value-of select="title"/>
			<xsl:text> </xsl:text>
			<xsl:value-of select="name"/>
		</para>
	</xsl:template>
	
	<xsl:template match="address" mode="shipping">
		<para style="address">
			<xsl:value-of select="title"/>
			<xsl:text> </xsl:text>
			<xsl:value-of select="name"/>
		</para>
		<para style="address">
			<xsl:value-of select="street"/>
		</para>
		<para style="address">
			<xsl:value-of select="zip"/>
			<xsl:text> </xsl:text>
			<xsl:value-of select="city"/>
		</para>
		<para style="address">
			<xsl:value-of select="country_id"/>
		</para>
	</xsl:template>
	
	<xsl:template match="address" mode="header">
		<xsl:value-of select="title"/>
		<xsl:text> </xsl:text>
		<xsl:value-of select="name"/>
	</xsl:template>
	
	<xsl:template match="lines">
		<spacer length="0.5cm"/>
	
		<setNextTemplate name="other_pages"/>
		<blockTable colWidths="2cm,2.2cm,2.2cm,2.5cm,2cm,4.5cm,2.1cm" style="products" repeatRows="1">
			<tr>
				<td t="1">Product</td>
				<td t="1">Tracking</td>
				<td t="1">Serial</td>
				<td t="1">Qty</td>
				<td t="1">Location</td>
				<td t="1">Description</td>
				<td t="1">State</td>
			</tr>
			<xsl:for-each select="line">
				<tr>
					<td><para style="prod"><xsl:value-of select="ref"/></para></td>
					<td><para style="prod"><xsl:value-of select="lot/tracking"/></para></td>
					<td><para style="prod"><xsl:value-of select="lot/serial"/></para></td>
					<td>
						<para style="prod-right">
							<xsl:value-of select="quantity"/>
							<xsl:text> </xsl:text>
							<xsl:value-of select="prod_uom"/>
						</para>
					</td>
					<td><para style="prod"><xsl:value-of select="location"/></para></td>
					<td><para style="prod"><xsl:value-of select="name"/><xsl:text> </xsl:text><xsl:value-of select="variant"/></para></td>
					<td><para style="prod-right"><xsl:value-of select="state"/></para></td>
				</tr>
			</xsl:for-each>
		</blockTable>

		<setNextTemplate name="first_page"/>
		<nextFrame/>
	</xsl:template>
	
</xsl:stylesheet>
