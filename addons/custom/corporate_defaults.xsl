<?xml version = '1.0' encoding="utf-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<xsl:variable name="signature" select="//corporate-header/user/signature"/>
	<xsl:variable name="title">Tiny ERP Report</xsl:variable>
	<xsl:variable name="leftMargin">1cm</xsl:variable>
	<xsl:variable name="rightMargin">1cm</xsl:variable>
	<xsl:variable name="topMargin">1cm</xsl:variable>
	<xsl:variable name="bottomMargin">1cm</xsl:variable>
	<xsl:variable name="pageSize">21cm,29.7cm</xsl:variable>

	<xsl:variable name="page_format">a4_letter</xsl:variable>

	<xsl:template name="first_page_graphics_corporation">
		<!--logo-->
		<setFont name="Helvetica" size="30"/>
		<fill color="darkblue"/>
		<stroke color="darkblue"/>
		<drawString x="1cm" y="27.8cm"><xsl:value-of select="//corporate-header/corporation/name"/></drawString>
		<lines>1cm 27.7cm 20cm 27.7cm</lines>
		<lines>1cm 25.7cm 7cm 25.7cm</lines>

		<setFont name="Helvetica" size="10"/>
		<drawRightString x="20cm" y="27.8cm"><xsl:value-of select="//corporate-header/corporation/rml_header1"/></drawRightString>
		<drawString x="1cm" y="27.1cm"><xsl:value-of select="//corporate-header/corporation/address/street"/></drawString>
		<drawString x="1cm" y="26.7cm">
			<xsl:value-of select="//corporate-header/corporation/address/zip"/>
			<xsl:text> </xsl:text>
			<xsl:value-of select="//corporate-header/corporation/address/city"/>
			<xsl:text> - </xsl:text>
			<xsl:value-of select="//corporate-header/corporation/address/country"/>
		</drawString>
		<drawString x="1cm" y="26.2cm">Phone:</drawString>
		<drawRightString x="7cm" y="26.2cm"><xsl:value-of select="//corporate-header/corporation/address/phone"/></drawRightString>
		<drawString x="1cm" y="25.8cm">Mail:</drawString>
		<drawRightString x="7cm" y="25.8cm"><xsl:value-of select="//corporate-header/corporation/address/email"/></drawRightString>

		<!--page bottom-->
		
		<lines>1.5cm 2.15cm 19.9cm 2.15cm</lines>
		
		<drawCentredString x="10.5cm" y="1.7cm"><xsl:value-of select="//corporate-header/corporation/rml_footer1"/></drawCentredString>
		<drawCentredString x="10.5cm" y="1.25cm"><xsl:value-of select="//corporate-header/corporation/rml_footer2"/></drawCentredString>
		<drawCentredString x="10.5cm" y="0.8cm">Your contact : <xsl:value-of select="//corporate-header/user/name"/></drawCentredString>
	</xsl:template>

	<xsl:template name="other_pages_graphics_corporation">
		<!--logo-->
		<setFont name="Helvetica" size="30"/>
		<fill color="darkblue"/>
		<stroke color="darkblue"/>
		<drawString x="1cm" y="27.8cm"><xsl:value-of select="//corporate-header/corporation/name"/></drawString>
		<lines>1cm 27.7cm 20cm 27.7cm</lines>
		<lines>1cm 25.7cm 7cm 25.7cm</lines>

		<setFont name="Helvetica" size="10"/>
		<drawRightString x="20cm" y="27.8cm"><xsl:value-of select="//corporate-header/corporation/rml_header1"/></drawRightString>
		<drawString x="1cm" y="27.1cm"><xsl:value-of select="//corporate-header/corporation/address/street"/></drawString>
		<drawString x="1cm" y="26.7cm">
			<xsl:value-of select="//corporate-header/corporation/address/zip"/>
			<xsl:value-of select="//corporate-header/corporation/address/city"/> - 
			<xsl:value-of select="//corporate-header/corporation/address/country"/>
		</drawString>
		<drawString x="1cm" y="26.2cm">Phone:</drawString>
		<drawRightString x="7cm" y="26.2cm"><xsl:value-of select="//corporate-header/corporation/address/phone"/></drawRightString>
		<drawString x="1cm" y="25.8cm">Mail:</drawString>
		<drawRightString x="7cm" y="25.8cm"><xsl:value-of select="//corporate-header/corporation/address/email"/></drawRightString>

		<!--page bottom-->
		
		<lines>1.5cm 2.15cm 19.9cm 2.15cm</lines>
		
		<drawCentredString x="10.5cm" y="1.7cm"><xsl:value-of select="//corporate-header/corporation/rml_footer1"/></drawCentredString>
		<drawCentredString x="10.5cm" y="1.25cm"><xsl:value-of select="//corporate-header/corporation/rml_footer2"/></drawCentredString>
		<drawCentredString x="10.5cm" y="0.8cm">Your contact : <xsl:value-of select="//corporate-header/user/name"/></drawCentredString>
	</xsl:template>

	<xsl:template name="first_page_frames">
		<xsl:if test="$page_format='a4_normal'">
			<frame id="main" x1="1cm" y1="2.5cm" width="19.0cm" height="22.0cm"/>
		</xsl:if>

		<xsl:if test="$page_format='a4_letter'">
			<frame id="address" x1="11cm" y1="21.5cm" width="6cm" height="4cm"/>
			<frame id="main" x1="1cm" y1="2.5cm" width="19.0cm" height="17.5cm"/>
		</xsl:if>
	</xsl:template>

	<xsl:template name="other_pages_frames">
		<frame id="main" x1="1cm" y1="2.5cm" width="19.0cm" height="22cm"/>
	</xsl:template>

</xsl:stylesheet>
