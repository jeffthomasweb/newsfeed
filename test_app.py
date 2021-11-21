import pytest
import feedparser
import re
from app import helloroc, news, rss 

#Sample RSS Feed below to test
rss_to_test = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:npr="https://www.npr.org/rss/" xmlns:nprml="https://api.npr.org/nprml" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
  <channel>
    <title>News : NPR</title>
    <link>https://www.npr.org/templates/story/story.php?storyId=1001</link>
    <description>NPR news, audio, and podcasts. Coverage of breaking stories, national and world news, politics, business, science, technology, and extended coverage of major national and world events.</description>
    <language>en</language>
    <copyright>Copyright 2021 NPR - For Personal Use Only</copyright>
    <generator>NPR API RSS Generator 0.94</generator>
    <lastBuildDate>Sat, 20 Nov 2021 16:24:45 -0500</lastBuildDate>
    <image>
      <url>https://media.npr.org/images/podcasts/primary/npr_generic_image_300.jpg?s=200</url>
      <title>News</title>
      <link>https://www.npr.org/templates/story/story.php?storyId=1001</link>
    </image>
    <item>
      <title>Atlanta's airport had an active shooter scare as millions prepare for holiday travel</title>
      <description>The accidental discharge of a weapon at the airport sent travelers into a panic Saturday, many taking to social media to alert other travelers to what they believed to be an active shooter situation.</description>
      <pubDate>Sat, 20 Nov 2021 16:24:45 -0500</pubDate>
      <link>https://www.npr.org/2021/11/20/1057661558/atlantas-airport-had-an-active-shooter-scare-as-millions-prepare-for-holiday-tra</link>
      <guid>https://www.npr.org/2021/11/20/1057661558/atlantas-airport-had-an-active-shooter-scare-as-millions-prepare-for-holiday-tra</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/20/gettyimages-94665297_wide-17986844b1c8c7d7ce93f4d8b98ce7a48730623b.jpg?s=600' alt='A TSA employee screens travelers at Hartsfield-Jackson International Airport in Atlanta, Ga., November 2007. TSA is expecting to screen 20 million travelers this Thanksgiving season.'/><p>The accidental discharge of a weapon at the airport sent travelers into a panic Saturday, many taking to social media to alert other travelers to what they believed to be an active shooter situation.</p><p>(Image credit: Chris Rank/Bloomberg via Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057661558' />]]></content:encoded>
      <dc:creator>Dustin Jones</dc:creator>
    </item>
    <item>
      <title>Kyle Rittenhouse verdict prompts protests in several cities</title>
      <description>Activists opposed to the jury's acquittal gathered in several cities across the country, including Chicago, New York and Oakland. Authorities in Portland declared a riot.</description>
      <pubDate>Sat, 20 Nov 2021 14:38:29 -0500</pubDate>
      <link>https://www.npr.org/2021/11/20/1057643957/kyle-rittenhouse-verdict-prompts-protests-in-several-cities</link>
      <guid>https://www.npr.org/2021/11/20/1057643957/kyle-rittenhouse-verdict-prompts-protests-in-several-cities</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/20/gettyimages-1236673226_wide-c8f5ca31ce9f4eb669694c17790165d000aa6f19.jpg?s=600' alt='A demonstrator raises her fist while marching on the street during a protest against the Kyle Rittenhouse not-guilty verdict near the Barclays Center in New York City on Friday.'/><p>Activists opposed to the jury's acquittal gathered in several cities across the country, including Chicago, New York and Oakland. Authorities in Portland declared a riot.</p><p>(Image credit: Yuki Iwamura/AFP via Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057643957' />]]></content:encoded>
      <dc:creator>Sharon Pruitt-Young</dc:creator>
    </item>
    <item>
      <title>Dutch police open fire on rioters in demonstration against COVID restrictions</title>
      <description>It was one of the worst outbreaks of violence in the Netherlands since coronavirus restrictions were first imposed last year. Police arrested 51 people in Rotterdam.</description>
      <pubDate>Sat, 20 Nov 2021 09:53:42 -0500</pubDate>
      <link>https://www.npr.org/2021/11/20/1057625905/dutch-police-open-fire-rioters-demonstration-covid-restrictions-rotterdam</link>
      <guid>https://www.npr.org/2021/11/20/1057625905/dutch-police-open-fire-rioters-demonstration-covid-restrictions-rotterdam</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/20/ap21323850456111_wide-60906b976e859d9541244b455823b654c4011f56.jpg?s=600' alt='In this image taken from video, demonstrators protest against government restrictions due to the coronavirus pandemic on Friday in Rotterdam, Netherlands.'/><p>It was one of the worst outbreaks of violence in the Netherlands since coronavirus restrictions were first imposed last year. Police arrested 51 people in Rotterdam.</p><p>(Image credit: Media TV Rotterdam via AP)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057625905' />]]></content:encoded>
      <dc:creator>The Associated Press</dc:creator>
    </item>
    <item>
      <title>Illinois Sen. Dick Durbin expects the Senate to pass spending bill by the end of 2021</title>
      <description>Sen. Dick Durbin, a Democrat from Illinois, spoke with NPR about how Democrats plan to secure all 50 member votes needed to pass President Biden's $2.2 trillion social spending bill.</description>
      <pubDate>Sat, 20 Nov 2021 08:50:00 -0500</pubDate>
      <link>https://www.npr.org/2021/11/20/1057619696/durbin</link>
      <guid>https://www.npr.org/2021/11/20/1057619696/durbin</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/20/gettyimages-1236301567_wide-a45cedd8c06ac0997e716361f9ca84e90e9d40d2.jpg?s=600' alt='Sen. Dick Durbin, D-Ill., says he believes the Senate will pass President Biden's spending bill before the end of the year. The House passed the bill on Friday, sending it to the 50-50 Senate.'/><p>Sen. Dick Durbin, a Democrat from Illinois, spoke with NPR about how Democrats plan to secure all 50 member votes needed to pass President Biden's $2.2 trillion social spending bill.</p><p>(Image credit: Pete Marovich/Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057619696' />]]></content:encoded>
      <dc:creator>Scott Simon</dc:creator>
    </item>
    <item>
      <title>Democrats hope Biden's sales job can help their midterm chances</title>
      <description>Democrats have spent months negotiating with themselves, undercutting their ability to take credit for bills of significance they are now passing, but for which they aren't getting credit.</description>
      <pubDate>Sat, 20 Nov 2021 07:01:20 -0500</pubDate>
      <link>https://www.npr.org/2021/11/20/1057537201/democrats-hope-bidens-sales-job-can-help-their-midterm-chances</link>
      <guid>https://www.npr.org/2021/11/20/1057537201/democrats-hope-bidens-sales-job-can-help-their-midterm-chances</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/ap_21323706838494_wide-44d9b613144e6770240f912feab48af2dc9c6d9c.jpg?s=600' alt='President Biden walks to speak with reporters as he returns to the White House Friday.'/><p>Democrats have spent months negotiating with themselves, undercutting their ability to take credit for bills of significance they are now passing, but for which they aren't getting credit.</p><p>(Image credit: Alex Brandon/AP)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057537201' />]]></content:encoded>
      <dc:creator>Mara Liasson</dc:creator>
    </item>
    <item>
      <title>Welcoming family into your home for Thanksgiving? Here's how to keep COVID out</title>
      <description>Intergenerational indoor gatherings, a.k.a, Thanksgiving dinner, still pose a COVID risk to older adults and the immunocompromised. Here's how to keep everyone safe.</description>
      <pubDate>Sat, 20 Nov 2021 07:00:20 -0500</pubDate>
      <link>https://www.npr.org/sections/health-shots/2021/11/20/1057237292/covid-risk-holidays-booster</link>
      <guid>https://www.npr.org/sections/health-shots/2021/11/20/1057237292/covid-risk-holidays-booster</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/covid-thanksgiving-1_wide-2cd9416c08079dab8bb7954375b0fb6579716205.jpg?s=600' alt='The holidays are upon us. Here's your toolkit for how to keep COVID out of your festivities and keep your most vulnerable family members safe this year.'/><p>Intergenerational indoor gatherings, a.k.a, Thanksgiving dinner, still pose a COVID risk to older adults and the immunocompromised. Here's how to keep everyone safe.</p><p>(Image credit: Chanelle Nibbelink for NPR)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057237292' />]]></content:encoded>
      <dc:creator>Allison Aubrey</dc:creator>
    </item>
    <item>
      <title>Prize-winning photos capture the grit and suffering of flood survivors in South Sudan</title>
      <description>The photo series &lt;em&gt;Unyielding Floods&lt;/em&gt; recently won its fifth award this year. It captures the strength and hardship of those affected by flooding of biblical proportions in South Sudan.</description>
      <pubDate>Sat, 20 Nov 2021 07:00:20 -0500</pubDate>
      <link>https://www.npr.org/sections/goatsandsoda/2021/11/20/1054865992/prize-winning-photos-capture-the-grit-and-suffering-of-flood-survivors-in-south-</link>
      <guid>https://www.npr.org/sections/goatsandsoda/2021/11/20/1054865992/prize-winning-photos-capture-the-grit-and-suffering-of-flood-survivors-in-south-</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/16/2021_11_15_sudan_peter_caton-1_wide-f1e64a38d80c7351a594ea20a42f4aff7f248b2c.jpg?s=600' alt='Nyayua Thang, 62, left, stands waist-deep in the floodwaters in front of an abandoned primary school in South Sudan. Members of her village, displaced by extreme flooding as a result of heavy rainfall, are using the building as a refuge. Only small mud dikes at the entrance of the door are keeping the water out. (November 2020)'/><p>The photo series <em>Unyielding Floods</em> recently won its fifth award this year. It captures the strength and hardship of those affected by flooding of biblical proportions in South Sudan.</p><p>(Image credit: Peter Caton for Action Against Hunger)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1054865992' />]]></content:encoded>
      <dc:creator>Diane Cole</dc:creator>
    </item>
    <item>
      <title>Giving up gas-powered cars was a fringe idea. It's now on its way to reality</title>
      <description>In just a few years, phasing out gas-powered cars has gone from fringe idea to mainstream policy proposal. It's still a long way from being reality, but the sense of urgency is accelerating.</description>
      <pubDate>Sat, 20 Nov 2021 05:00:20 -0500</pubDate>
      <link>https://www.npr.org/2021/11/20/1055718914/giving-up-gas-powered-cars-for-electric-vehicles</link>
      <guid>https://www.npr.org/2021/11/20/1055718914/giving-up-gas-powered-cars-for-electric-vehicles</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/ap_21203825749056_wide-5f5d81d953c01ea1a62f1775a374879dd0004ea4.jpg?s=600' alt='Motorists fill up their vehicles at a Shell station on July 22 in Denver. Phasing out the sale of gas-powered cars once seemed laughable. It's now inching closer to reality.'/><p>In just a few years, phasing out gas-powered cars has gone from fringe idea to mainstream policy proposal. It's still a long way from being reality, but the sense of urgency is accelerating.</p><p>(Image credit: David Zalubowski/AP)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1055718914' />]]></content:encoded>
      <dc:creator>Camila Domonoske</dc:creator>
    </item>
    <item>
      <title>Elizabeth Holmes takes the stand in her criminal fraud trial</title>
      <description>The surprise decision to have Holmes testify so early came as a bombshell and carries considerable risk. Prosecutors have made it clear that they're eager to grill Holmes under oath.</description>
      <pubDate>Fri, 19 Nov 2021 20:59:12 -0500</pubDate>
      <link>https://www.npr.org/2021/11/19/1057530276/elizabeth-holmes-takes-the-stand-criminal-fraud-trial-theranos</link>
      <guid>https://www.npr.org/2021/11/19/1057530276/elizabeth-holmes-takes-the-stand-criminal-fraud-trial-theranos</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/ap21323682851514-1-_wide-ae8f1c04b5a90bf113083f1a7a9592d3e8fe7717.jpg?s=600' alt='Elizabeth Holmes, pictured in May 2021, took the stand on Friday.'/><p>The surprise decision to have Holmes testify so early came as a bombshell and carries considerable risk. Prosecutors have made it clear that they're eager to grill Holmes under oath.</p><p>(Image credit: Nhat V. Meyer/Bay Area News Group via AP)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057530276' />]]></content:encoded>
      <dc:creator>The Associated Press</dc:creator>
    </item>
    <item>
      <title>For far-right groups, Rittenhouse's acquittal is a cause for celebration</title>
      <description>One expert fears that the acquittal of Kyle Rittenhouse will embolden people to seek out altercations where it could be possible to make claims of self-defense.</description>
      <pubDate>Fri, 19 Nov 2021 19:07:46 -0500</pubDate>
      <link>https://www.npr.org/2021/11/19/1057478725/far-right-groups-rittenhouse-acquittal-celebration-violence</link>
      <guid>https://www.npr.org/2021/11/19/1057478725/far-right-groups-rittenhouse-acquittal-celebration-violence</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/ap20274126061619_wide-89f9c162596f8ca23335fcdd0b17a825bbca5ac3.jpg?s=600' alt='Armed participants walk at a Proud Boys rally with other right-wing demonstrators in September 2020 in Portland, Ore. Far-right groups celebrated the verdict in the Rittenhouse trial.'/><p>One expert fears that the acquittal of Kyle Rittenhouse will embolden people to seek out altercations where it could be possible to make claims of self-defense.</p><p>(Image credit: John Locher/AP)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057478725' />]]></content:encoded>
      <dc:creator>Odette Yousef</dc:creator>
    </item>
    <item>
      <title>Rock is dead, but the photographer's iconic images of Bowie, Blondie and more live on</title>
      <description>Mick Rock, iconic photographer of rock stars, has died. He was known for his images of David Bowie, Lou Reed, Queen and Blondie. He was 72.</description>
      <pubDate>Fri, 19 Nov 2021 17:52:42 -0500</pubDate>
      <link>https://www.npr.org/2021/11/19/1057450818/mick-rock-photographer-bowie-queen-blondie-dead</link>
      <guid>https://www.npr.org/2021/11/19/1057450818/mick-rock-photographer-bowie-queen-blondie-dead</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/gettyimages-487497076_wide-61fa5b9f6d248a1b78b91b61b376e5f6e2b90984.jpg?s=600' alt='Photographer Mick Rock at the opening reception for Mick Rock: Shooting For Stardust - The Rise Of David Bowie & Co. in Los Angeles in 2015.'/><p>Mick Rock, iconic photographer of rock stars, has died. He was known for his images of David Bowie, Lou Reed, Queen and Blondie. He was 72.</p><p>(Image credit: Angela Weiss/Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057450818' />]]></content:encoded>
      <dc:creator>Elizabeth Blair</dc:creator>
    </item>
    <item>
      <title>Why the Kyle Rittenhouse 'not guilty' verdict is not a surprise to legal experts</title>
      <description>Prosecutors had argued that Rittenhouse was responsible for the deadly peril that night. But legal experts said his claim of self-defense was strong from the beginning.</description>
      <pubDate>Fri, 19 Nov 2021 17:40:00 -0500</pubDate>
      <link>https://www.npr.org/2021/11/19/1057422329/why-legal-experts-were-not-surprised-by-the-rittenhouse-jurys-decision-to-acquit</link>
      <guid>https://www.npr.org/2021/11/19/1057422329/why-legal-experts-were-not-surprised-by-the-rittenhouse-jurys-decision-to-acquit</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/gettyimages-1236665299_wide-7f72d1c9dce51e53169565256e9cdc53b685ebd3.jpg?s=600' alt='Bystanders on the steps of the courthouse watch as the verdict is read in the trial of Kyle Rittenhouse. Legal experts said Rittenhouse's claim of self-defense was strong from the beginning.'/><p>Prosecutors had argued that Rittenhouse was responsible for the deadly peril that night. But legal experts said his claim of self-defense was strong from the beginning.</p><p>(Image credit: Nathan Howard/Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057422329' />]]></content:encoded>
      <dc:creator>Becky Sullivan</dc:creator>
    </item>
    <item>
      <title>Research sheds light on what's killing young people, especially boys and young men</title>
      <description>Globally, boys and young men made up two-thirds of all deaths among young people in 2019. A recent report finds that many such deaths in this "neglected" age group are preventable.</description>
      <pubDate>Fri, 19 Nov 2021 17:35:31 -0500</pubDate>
      <link>https://www.npr.org/sections/goatsandsoda/2021/11/19/1055129130/research-sheds-light-on-whats-killing-young-people-especially-boys-and-young-men</link>
      <guid>https://www.npr.org/sections/goatsandsoda/2021/11/19/1055129130/research-sheds-light-on-whats-killing-young-people-especially-boys-and-young-men</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/gettyimages-1233825014-40_wide-38cfbdf37daf6ac1c3c575666de40a99fa68bbf3.jpg?s=600' alt='Two boys stand at the edge of the Buriganga River in Dhaka, Bangladesh, in July. A recent study finds that globally, boys and young men made up two-thirds of all deaths among young people in 2019.'/><p>Globally, boys and young men made up two-thirds of all deaths among young people in 2019. A recent report finds that many such deaths in this "neglected" age group are preventable.</p><p>(Image credit: Kazi Salahuddin Razu/NurPhoto via Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1055129130' />]]></content:encoded>
      <dc:creator>Joanne Silberner</dc:creator>
    </item>
    <item>
      <title>Interior Secretary Deb Haaland moves to ban the word 'squaw' from federal lands</title>
      <description>"Racist terms have no place in our vernacular or on our federal lands," Secretary of the Interior Deb Haaland said as she formally declared "squaw" to be a derogatory term.</description>
      <pubDate>Fri, 19 Nov 2021 16:29:47 -0500</pubDate>
      <link>https://www.npr.org/2021/11/19/1057367325/interior-secretary-deb-haaland-moves-to-ban-the-word-squaw-from-federal-lands</link>
      <guid>https://www.npr.org/2021/11/19/1057367325/interior-secretary-deb-haaland-moves-to-ban-the-word-squaw-from-federal-lands</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/gettyimages-1236582897_wide-3941d82c7e4d7dcf2043fae14ecfc9e51ed25ef8.jpg?s=600' alt='"Our nation's lands and waters should be places to celebrate the outdoors and our shared cultural heritage — not to perpetuate the legacies of oppression," Secretary of the Interior Deb Haaland said as she ordered the word "squaw" to be removed from federal place names.'/><p>"Racist terms have no place in our vernacular or on our federal lands," Secretary of the Interior Deb Haaland said as she formally declared "squaw" to be a derogatory term.</p><p>(Image credit: Mandel Ngan/AFP via Getty Images)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057367325' />]]></content:encoded>
      <dc:creator>Bill Chappell</dc:creator>
    </item>
    <item>
      <title>President Biden pardons turkeys, Peanut Butter and Jelly, ahead of Thanksgiving </title>
      <description>In President Biden's first turkey pardon, he spared two turkeys from the Thanksgiving dinner table. The turkeys' names — Peanut Butter and Jelly — were from a list submitted by schoolchildren.</description>
      <pubDate>Fri, 19 Nov 2021 16:14:22 -0500</pubDate>
      <link>https://www.npr.org/2021/11/19/1057289605/president-biden-pardons-turkeys-peanut-butter-and-jelly-ahead-of-thanksgiving</link>
      <guid>https://www.npr.org/2021/11/19/1057289605/president-biden-pardons-turkeys-peanut-butter-and-jelly-ahead-of-thanksgiving</guid>
      <content:encoded><![CDATA[<img src='https://media.npr.org/assets/img/2021/11/19/ap21323742716368_wide-2c5dd666319e770f57ae12f083dd356abb702311.jpg?s=600' alt='The two national Thanksgiving turkeys are seen in the Rose Garden of the White House before a pardon ceremony in Washington on Nov. 19, 2021.'/><p>In President Biden's first turkey pardon, he spared two turkeys from the Thanksgiving dinner table. The turkeys' names — Peanut Butter and Jelly — were from a list submitted by schoolchildren.</p><p>(Image credit: Susan Walsh/AP)</p><img src='https://media.npr.org/include/images/tracking/npr-rss-pixel.png?story=1057289605' />]]></content:encoded>
      <dc:creator>Tien Le</dc:creator>
    </item>
  </channel>
</rss>"""

#variables b, b1, and b2 are sample strings to test using regular expressions to remove errant <em> and </em> tags that the feedparser library may not remove
#b is a string with <em> and </em> tags
b = "President Biden pardons turkeys, <em>Peanut Butter</em> and Jelly, ahead of Thanksgiving. In President Biden's first turkey pardon, he spared two turkeys from the Thanksgiving dinner table. The turkeys' names — Peanut Butter and Jelly — were from a list submitted by schoolchildren."

#b1 is the resulting string of removing the <em> tag from variable b
b1 = f"President Biden pardons turkeys, Peanut Butter</em> and Jelly, ahead of Thanksgiving. In President Biden's first turkey pardon, he spared two turkeys from the Thanksgiving dinner table. The turkeys' names — Peanut Butter and Jelly — were from a list submitted by schoolchildren."

#b2 is a string that has the </em> tag removed
b2 = f"President Biden pardons turkeys, Peanut Butter and Jelly, ahead of Thanksgiving. In President Biden's first turkey pardon, he spared two turkeys from the Thanksgiving dinner table. The turkeys' names — Peanut Butter and Jelly — were from a list submitted by schoolchildren."

#Use regular expressions to remove the <em> tag from string b
b_em_removed1 = re.sub('<em>', '',b)

#Use regular expressions to remove the </em> tag from string b_em_removed1
b_em_removed2 = re.sub('</em>', '',b_em_removed1)

#Test that story 15 in the test RSS feed (the index of story 15 is 14) is parsed correctly
def test_feed():
    a = feedparser.parse(rss_to_test)
    story_15_parsed = f"{a.entries[14].title + '. ' + a.entries[14].summary}"
    assert story_15_parsed == "President Biden pardons turkeys, Peanut Butter and Jelly, ahead of Thanksgiving. In President Biden's first turkey pardon, he spared two turkeys from the Thanksgiving dinner table. The turkeys' names — Peanut Butter and Jelly — were from a list submitted by schoolchildren." 

#Test route /hi
def test_hello():
    assert helloroc() == "Hello RocPy 🪨🐍!"

#Test function to test regular expressions removing the <em> tag    
def test_re1():
    assert b_em_removed1 == b1

#Test function to test regular expressions removing the </em> tag
def test_re2():
    assert b_em_removed2 == b2
