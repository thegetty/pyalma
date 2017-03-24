[![Build Status](https://travis-ci.org/gri-is/pyalma.svg?branch=master)](https://travis-ci.org/gri-is/pyalma)

[![Coverage Status](https://coveralls.io/repos/github/gri-is/pyalma/badge.svg?branch=master)](https://coveralls.io/github/gri-is/pyalma?branch=master)

PyAlma
======

Developer Installation
----------------------

0. Ensure that Python 3 is installed on your machine (https://www.python.org/downloads/)

1. Create a directory for development projects on your machine

        $ mkdir /<path on your machine>/projects
        $ cd /<path>/projects

2. Clone the repository

        $ git clone https://<your login>@stash.getty.edu/scm/griis/pyalma.git
        $ cd pyalma

3. Create a virtual environment and activate it

        $ pyvenv ENV
        $ source ENV/bin/activate

4. Install dependencies to the virtual environment

        (ENV)$ pip install -r requirements.txt

5. Run the tests to make sure everything works correctly

        (ENV)$ python -m unittest

Developer Changes
-----------------

6. When working on a new issue, be sure to do so in a new branch

        (ENV)$ git branch <issue-name>
        (ENV)$ git checkout <issue-name>

7. Run a status check before doing any adds, commits or pushes

        (ENV)$ git status

8. Stage edited or newly created files

        (ENV)$ git status
        (ENV)$ git add <name of file>

9. Commit the staged changes and ALWAYS explain the changes in a message

        (ENV)$ git status
        (ENV)$ git commit -m <message>

10. Push the changes to the shared repository, using the same branch name

        (ENV)$ git status
        (ENV)$ git push origin <issue-name>

11. On the repository website create a pull request from your branch to the master branch

12. When your branch has been reviewed, approved, and merged, you can pull the master and delete your issue branch

        (ENV)$ git checkout master
        (ENV)$ git status
        (ENV)$ git pull origin master
        (ENV)$ git branch -d <issue-name>


API KEY Configuration
---------------------

The Alma API requires a secret API key. You must also point to correct regional endpoint, of which there are three:

1. US: https://api-na.hosted.exlibrisgroup.com
2. EU: https://api-eu.hosted.exlibrisgroup.com
3. APAC: https://api-ap.hosted.exlibrisgroup.com

You can pass the key and region directly to the Alma object at the time of creation, like so:

    from pyalma.alma import Alma
    api = alma.Alma(apikey='xxxxxxxxxx', region='US')

Or, you can create environment variables in your operating system and the Python client will find it. On a linux machine you can do this by editing the `/etc/environment` file, like so:

    ALMA_API_KEY=xxxxxxxxx
    ALMA_API_REGION=US

After editing the `/etc/environment` file, be sure to reload it, like so:

    :$ source /etc/environment

For Mac OSX, this may be slightly different. This document may be of some help: http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-mac-os-x-terminal-only/

PyAlma Usage Example:
---------------------

1. After starting up a Python session, import the library and create an api object:

        >>> from pyalma.alma import Alma
        >>> api = Alma()

   Note: you can only do the above if you set your environment as described above. Otherwise you have to pass in your API key and region like so:

        >>> api = alma.Alma(apikey='xxxxxxxxxx', region='US')

2. Now go get your record:

         >>> bib = api.get_bib('9927390750001551')

   Note: The bib is in json format by default unless you pass in accept='xml' to the method.

3. To see the content of the bib you can print it:

        >>> from pprint import pprint
        >>> pprint(bib)
        {'anies': ['<?xml version="1.0" encoding="UTF-16"?>\n'
           '<record><leader>01523cam a2200481 a 4500</leader><controlfield '
           'tag="001">9927390750001551</controlfield><controlfield '
           'tag="005">20160713120531.0</controlfield><controlfield '
           'tag="008">940411s1992    cs a     c    000 0 cze  '
           '</controlfield><controlfield '
           'tag="009">337522</controlfield><datafield ind1=" " ind2=" " '
           'tag="010"><subfield '
           'code="a">93225732</subfield></datafield><datafield ind1=" " ind2=" '
           '" tag="035"><subfield '
           'code="9">94-B7378</subfield></datafield><datafield ind1=" " ind2=" '
           '" tag="035"><subfield '
           'code="a">337522</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="035"><subfield '
           'code="a">(CMalG)337522-gettydb-Voyager</subfield></datafield><datafield '
           'ind1=" " ind2=" " tag="035"><subfield '
           'code="a">(OCoLC)29550137</subfield></datafield><datafield ind1=" " '
           'ind2=" " tag="040"><subfield code="a">DLC</subfield><subfield '
           'code="c">DLC</subfield><subfield '
           'code="d">CMalG</subfield></datafield><datafield ind1="0" ind2=" " '
           'tag="041"><subfield '
           'code="a">czeengfregeritaspa</subfield></datafield><datafield '
           'ind1="0" ind2="0" tag="050"><subfield '
           'code="a">N6834.5.M8</subfield><subfield code="b">A4 '
           '1992</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="090"><subfield code="a">N6834.5.M8</subfield><subfield '
           'code="b">A4 1992</subfield></datafield><datafield ind1="1" ind2=" '
           '" tag="100"><subfield code="a">Kusák, '
           'Dalibor.</subfield></datafield><datafield ind1="1" ind2="0" '
           'tag="245"><subfield code="a">Mucha /</subfield><subfield '
           'code="c">Dalibor Kusák, Marta '
           'Kadlečíková.</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="250"><subfield code="a">Vyd. '
           '1.</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="260"><subfield code="a">Prague :</subfield><subfield '
           'code="b">BB/art,</subfield><subfield '
           'code="c">1992.</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="300"><subfield code="a">1 v. (unpaged) :</subfield><subfield '
           'code="b">chiefly col. ill. ;</subfield><subfield code="c">31 '
           'cm.</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="500"><subfield code="a">Text in Czech, English, French, '
           'German, Italian, and Spanish.</subfield></datafield><datafield '
           'ind1="1" ind2="0" tag="600"><subfield code="a">Mucha, '
           'Alphonse,</subfield><subfield '
           'code="d">1860-1939</subfield><subfield '
           'code="x">Catalogs.</subfield></datafield><datafield ind1="1" '
           'ind2=" " tag="700"><subfield code="a">Kadlečíková, '
           'Marta.</subfield></datafield><datafield ind1="1" ind2=" " '
           'tag="700"><subfield code="a">Mucha, Alphonse,</subfield><subfield '
           'code="d">1860-1939.</subfield></datafield><datafield ind1=" " '
           'ind2="1" tag="905"><subfield code="a">1</subfield><subfield '
           'code="b">04/11/94 AGR</subfield><subfield '
           'code="c">MAI</subfield><subfield '
           'code="e">DA</subfield></datafield><datafield ind1=" " ind2="1" '
           'tag="906"><subfield code="a">WSM</subfield></datafield><datafield '
           'ind1=" " ind2="1" tag="907"><subfield '
           'code="b">LGET02</subfield></datafield><datafield ind1=" " ind2="1" '
           'tag="908"><subfield '
           'code="a">pr/140.00,zc/gdm,inv#2652,invd940307,inrd940411</subfield></datafield><datafield '
           'ind1=" " ind2="1" tag="909"><subfield '
           'code="a">JME</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="911"><subfield code="a">OCLC REC '
           'TEST</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="921"><subfield code="a">b13412863</subfield><subfield '
           'code="b">02-20-97</subfield><subfield '
           'code="c">04-28-95</subfield><subfield '
           'code="d">cc</subfield><subfield '
           'code="e">01-01-95</subfield><subfield '
           'code="f">a</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="935"><subfield code="a">c</subfield></datafield><datafield '
           'ind1=" " ind2=" " tag="948"><subfield code="a">OCLC '
           'D160706.R807645 20160708</subfield></datafield><datafield ind1=" " '
           'ind2=" " tag="950"><subfield '
           'code="l">MAIN</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="955"><subfield code="c">1</subfield><subfield '
           'code="q">94-B7378-1</subfield><subfield '
           'code="r">33125007037290</subfield><subfield code="i">04/13/94 '
           'C</subfield></datafield><datafield ind1=" " ind2="1" '
           'tag="955"><subfield '
           'code="r">33125007037290</subfield></datafield><datafield ind1=" " '
           'ind2="1" tag="960"><subfield '
           'code="b">0</subfield></datafield><datafield ind1=" " ind2="1" '
           'tag="981"><subfield code="b">1</subfield><subfield '
           'code="c">04/13/94 CAT</subfield><subfield '
           'code="d">MAIN</subfield><subfield '
           'code="e">MAIN</subfield><subfield code="i">04/11/94 '
           'REC</subfield></datafield><datafield ind1=" " ind2=" " '
           'tag="995"><subfield '
           'code="a">94-B07378</subfield></datafield><datafield ind1=" " '
           'ind2=" " tag="998"><subfield code="s">9110</subfield><subfield '
           'code="n">CMalG</subfield><subfield '
           'code="c">AGR</subfield><subfield code="b">GCS</subfield><subfield '
           'code="l">CJPA</subfield></datafield></record>'],
         'author': 'Kusák, Dalibor.',
         'complete_edition': 'Vyd. 1.',
         'created_by': 'import',
         'created_date': '2013-07-14Z',
         'holdings': {'link': 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/9927390750001551/holdings',
                      'value': None},
         'isbn': None,
         'issn': None,
         'last_modified_by': 'System',
         'last_modified_date': '2016-07-13Z',
         'link': None,
         'linked_record_id': {'type': None, 'value': None},
         'mms_id': '9927390750001551',
         'network_number': ['(OCoLC)29550137',
                            '(CMalG)337522-gettydb-Voyager',
                            '337522'],
         'originating_system': 'OTHER',
         'originating_system_id': '337522-gettydb',
         'place_of_publication': 'Prague :',
         'publisher_const': 'BB/art',
         'record_format': 'marc21',
         'suppress_from_publishing': 'false',
         'title': 'Mucha /'}

   Note: the MARC data appears as an XML string inside the JSON.

4. There is also a convenience method that converts the JSON to a custom Bib record object. That Bib object also has the MARXML converted to a pymarc object.  Use bib() instead of get_bib().

        >>> bib = api.bib('9927390750001551')
        >>> bib
        <pyalma.records.Bib object at 0x7f3ecfa6c278>
        >>> bib.marc
        <pymarc.record.Record object at 0x7f3ecfa82470>

        >>> bib.marc.author()
        'Kusák, Dalibor.'

        >>> print(bib.marc)
        =LDR  01523cam a2200481 a 4500
        =001  9927390750001551
        =005  20160713120531.0
        =008  940411s1992\\\\cs\a\\\\\c\\\\000\0\cze\\
        =009  337522
        =010  \\$a93225732
        =035  \\$994-B7378
        =035  \\$a337522
        =035  \\$a(CMalG)337522-gettydb-Voyager
        =035  \\$a(OCoLC)29550137
        =040  \\$aDLC$cDLC$dCMalG
        =041  0\$aczeengfregeritaspa
        =050  00$aN6834.5.M8$bA4 1992
        =090  \\$aN6834.5.M8$bA4 1992
        =100  1\$aKusák, Dalibor.
        =245  10$aMucha /$cDalibor Kusák, Marta Kadlečíková.
        =250  \\$aVyd. 1.
        =260  \\$aPrague :$bBB/art,$c1992.
        =300  \\$a1 v. (unpaged) :$bchiefly col. ill. ;$c31 cm.
        =500  \\$aText in Czech, English, French, German, Italian, and Spanish.
        =600  10$aMucha, Alphonse,$d1860-1939$xCatalogs.
        =700  1\$aKadlečíková, Marta.
        =700  1\$aMucha, Alphonse,$d1860-1939.
        =905  \1$a1$b04/11/94 AGR$cMAI$eDA
        =906  \1$aWSM
        =907  \1$bLGET02
        =908  \1$apr/140.00,zc/gdm,inv#2652,invd940307,inrd940411
        =909  \1$aJME
        =911  \\$aOCLC REC TEST
        =921  \\$ab13412863$b02-20-97$c04-28-95$dcc$e01-01-95$fa
        =935  \\$ac
        =948  \\$aOCLC D160706.R807645 20160708
        =950  \\$lMAIN
        =955  \\$c1$q94-B7378-1$r33125007037290$i04/13/94 C
        =955  \1$r33125007037290
        =960  \1$b0
        =981  \1$b1$c04/13/94 CAT$dMAIN$eMAIN$i04/11/94 REC
        =995  \\$a94-B07378
        =998  \\$s9110$nCMalG$cAGR$bGCS$lCJPA[\\$s9110$nCMalG$cAGR$bGCS$lCJPA]


