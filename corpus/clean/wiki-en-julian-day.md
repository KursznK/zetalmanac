# Julian day

The Julian day is a continuous count of days from the beginning of the Julian period; it is used primarily by astronomers, and in software for easily calculating elapsed days between two events (e.g., food production date and expiration date).
The Julian period is a chronological interval of 7980 years, derived from three multi-year cycles: the indiction, solar, and lunar cycles. The last year that was simultaneously the beginning of all three cycles was 4713 BC (−4712), so that is year 1 of the current Julian period, making AD 2026 year 6739 of that Period. The next Julian period begins in the year AD 3268. Historians used the period to identify Julian calendar years within which an event occurred when no such year was given in the historical record, or when the year given by previous historians was incorrect.
The Julian day number (JDN) has the same epoch as the Julian period, but counts the number of days since the epoch rather than the number of years since then. Specifically, Julian day number 0 is assigned to the day starting at noon Universal Time on Monday, 1 January 4713 BC, proleptic Julian calendar (24 November 4714 BC, in the proleptic Gregorian calendar). For example, the Julian day number for the day starting at 12:00 UT (noon) on 1 January 2000, was 2451545.
The Julian date (JD) of any instant is the Julian day number plus the fraction of a day since the preceding noon in Universal Time. Julian dates are expressed as a Julian day number with a decimal fraction added. For example, the Julian Date for 00:30:00.0 UT 1 January 2013, is 2456293.520833. This article was loaded at 2026-11-05 21:31:08 (UTC) – expressed as a Julian date this is 2461350.3966204.


== Terminology ==
The term Julian date may also refer, outside of astronomy, to the day-of-year number (more properly, the ordinal date) in the Gregorian calendar, especially in computer programming, the military and the food industry, or it may refer to dates in the Julian calendar. For example, if a given "Julian date" is "5 October 1582", this means that date is in the Julian calendar (which was 15 October 1582, in the Gregorian calendar – the date it was first established). Without an astronomical or historical context, a "Julian date" given as "36" most likely means the 36th day of a given Gregorian year, namely 5 February. Other possible meanings of a "Julian date" of "36" include an astronomical Julian Day Number, or the year AD 36 in the Julian calendar, or a duration of 36 astronomical Julian years. This is why the terms "ordinal date" or "day-of-year" are preferred. In contexts where a "Julian date" means simply an ordinal date, calendars of a Gregorian year with formatting for ordinal dates are often called "Julian calendars", but this could also mean that the calendars are of years in the Julian calendar system.
Historically, Julian dates were recorded relative to Greenwich Mean Time (GMT) (later, Ephemeris Time), but since 1997 the International Astronomical Union has recommended that Julian dates be specified in Terrestrial Time. Seidelmann indicates that Julian dates may be used with International Atomic Time (TAI), Terrestrial Time (TT), Barycentric Coordinate Time (TCB), or Coordinated Universal Time (UTC) and that the scale should be indicated when the difference is significant. The fraction of the day is found by converting the number of hours, minutes, and seconds after noon into the equivalent decimal fraction. Time intervals calculated from differences of Julian Dates specified in non-uniform time scales, such as UTC, may need to be corrected for changes in time scales (e.g. leap seconds).


== Variants ==

Because the starting point or reference epoch is so long ago, numbers in the Julian day can be quite large and cumbersome. A more recent starting point is sometimes used, for instance by dropping the leading digits, in order to fit into limited computer memory with an adequate amount of precision. In the following table, times are given in 24-hour notation.
In the table below, Epoch refers to the point in time used to set the origin (usually zero, but (1) where explicitly indicated) of the alternative convention being discussed in that row. The date given is a Gregorian calendar date unless otherwise specified. JD stands for Julian Date. 0h is 00:00 midnight, 12h is 12:00 noon, UT unless otherwise specified. Current value is at 21:31, Thursday, November 5, 2026 (UTC) and may be cached. []

The Modified Julian Date (MJD) was introduced by the Smithsonian Astrophysical Observatory in 1957 to record the orbit of Sputnik via an IBM 704 (36-bit machine) and using only 18 bits until 7 August 2576. MJD is the epoch of VAX/VMS and its successor OpenVMS, using 63-bit date/time, which allows times to be stored up to 31 July 31086, 02:48:05.47. The MJD has a starting point of midnight on 17 November 1858, and is computed by MJD = JD − 2400000.5 
The Truncated Julian Day (TJD) was introduced by NASA/Goddard in 1979 as part of a parallel grouped binary time code (PB-5) "designed specifically, although not exclusively, for spacecraft applications". TJD was a 4-digit day count from MJD 40000, which was 24 May 1968, represented as a 14-bit binary number. Since this code was limited to four digits, TJD recycled to zero on MJD 50000, or 10 October 1995, "which gives a long ambiguity period of 27.4 years". (NASA codes PB-1–PB-4 used a 3-digit day-of-year count.) Only whole days are represented. Time of day is expressed by a count of seconds of a day, plus optional milliseconds, microseconds and nanoseconds in separate fields. Later PB-5J was introduced which increased the TJD field to 16 bits, allowing values up to 65535, which will occur in the year 2147. There are five digits recorded after TJD 9999.
The Dublin Julian Date (DJD) is the number of days that has elapsed since the epoch of the solar and lunar ephemerides used from 1900 through 1983, Newcomb's Tables of the Sun and Ernest W. Brown's Tables of the Motion of the Moon (1919). This epoch was noon UT on January 0, 1900, which is the same as noon UT on 31 December 1899. The DJD was defined by the International Astronomical Union at their meeting in Dublin, Ireland, in 1955.
The Lilian day number is a count of days of the Gregorian calendar and not defined relative to the Julian Date. It is an integer applied to a whole day; day 1 was 15 October 1582, which was the day the Gregorian calendar went into effect. The original paper defining it makes no mention of the time zone, and no mention of time-of-day. It was named for Aloysius Lilius, the principal author of the Gregorian calendar.
Rata Die is a system used in Rexx, Go and Python. Some implementations or options use Universal Time, others use local time. Day 1 is 1 January 1, that is, the first day of the Christian or Common Era in the proleptic Gregorian calendar. In Rexx, 1 January is Day 0.
The Heliocentric Julian Day (HJD) is the same as the Julian day, but adjusted to the frame of reference of the Sun, and thus can differ from the Julian day by as much as 8.3 minutes (498 seconds), that being the time it takes light to reach Earth from the Sun.


== History ==


=== Julian period ===
The Julian day number is based on the Julian period proposed by Joseph Scaliger, a classical scholar, in 1583 (one year after the Gregorian calendar reform) as it is the product of three calendar cycles used with the Julian calendar:

Its epoch occurs when all three cycles (if they are continued backward far enough) were in their first year together. Years of the Julian period are counted from this year, 4713 BC, as year 1, which was chosen to be before any historical record.
Scaliger corrected chronology by assigning each year a tricyclic "character", three numbers indicating that year's position in the 28-year solar cycle, the 19-year lunar cycle, and the 15-year indiction cycle. One or more of these numbers often appeared in the historical record alongside other pertinent facts without any mention of the Julian calendar year. The character of every year in the historical record was unique – it could only belong to one year in the 7980-year Julian period. Scaliger determined that 1 BC or year 0 was Julian period (JP) 4713. He knew that 1 BC or year 0 had the character 9 of the solar cycle, 1 of the lunar cycle, and 3 of the indiction cycle. By inspecting a 532-year Paschal cycle with 19 solar cycles (each of 28 years, each year numbered 1–28) and 28 lunar cycles (each of 19 years, each year numbered 1–19), he determined that the first two numbers, 9 and 1, occurred at its year 457. He then calculated via remainder division that he needed to add eight 532-year Paschal cycles totaling 4256 years before the cycle containing 1 BC or year 0 in order for its year 457 to be indiction 3. The sum 4256 + 457 was thus JP 4713.
A formula for determining the year of the Julian period given its character involving three four-digit numbers was published by Jacques de Billy in 1665 in the Philosophical Transactions of the Royal Society (its first year). John F. W. Herschel gave the same formula using slightly different wording in his 1849 Outlines of Astronomy.

Multiply the Solar Cycle by 4845, and the Lunar, by 4200, and that of the Indiction, by 6916. Then divide the Sum of the products by 7980, which is the Julian Period: The Remainder of the Division, without regard to the Quotient, shall be the year enquired after.
Carl Friedrich Gauss introduced the modulo operation in 1801, restating de Billy's formula as: 

where a is the year of the indiction cycle, b of the lunar cycle, and c of the solar cycle.
John Collins described the details of how these three numbers were calculated in 1666, using many trials. A summary of Collin's description is in a footnote.
Reese, Everett and Craun reduced the dividends in the Try column from 285, 420, 532 to 5, 2, 7 and changed remainder to modulo, but apparently still required many trials.
The specific cycles used by Scaliger to form his tricyclic Julian period were, first, the indiction cycle with a first year of 313. Then he chose the dominant 19-year Alexandrian lunar cycle with a first year of 285, the Era of Martyrs and the Diocletian Era epoch, or a first year of 532 according to Dionysius Exiguus. Finally, Scaliger chose the post-Bedan solar cycle with a first year of 776, when its first quadrennium of concurrents, 1 2 3 4, began in sequence. Although not their intended use, the equations of de Billy or Gauss can be used to determined the first year of any 15-, 19-, and 28-year tricyclic period given any first years of their cycles. For those of the Julian period, the result is AD 3268, because both remainder and modulo usually return the lowest positive result. Thus 7980 years must be subtracted from it to yield the first year of the present Julian period, −4712 or 4713 BC, when all three of its sub-cycles are in their first years.
Scaliger got the idea of using a tricyclic period from "the Greeks of Constantinople" as Herschel stated in his quotation below in Julian day numbers. Specifically, the monk and priest Georgios wrote in 638/39 that the Byzantine year 6149 AM (640/41) had indiction 14, lunar cycle 12, and solar cycle 17, which places the first year of the Byzantine Era in 5509/08 BC, the Byzantine Creation. Dionysius Exiguus called the Byzantine lunar cycle his "lunar cycle" in argumentum 6, in contrast with the Alexandrian lunar cycle which he called his "nineteen-year cycle" in argumentum 5.
Although many references say that the Julian in "Julian period" refers to Scaliger's father, Julius Scaliger, at the beginning of Book V of his Opus de Emendatione Temporum ("Work on the Emendation of Time") he states, "Iulianam vocauimus: quia ad annum Iulianum accomodata", which Reese, Everett and Craun translate as "We have termed it Julian because it fits the Julian year". Thus Julian refers to the Julian calendar.


=== Julian day numbers ===
Julian days were first used by Ludwig Ideler for the first days of the Nabonassar and Christian eras in his 1825 Handbuch der mathematischen und technischen Chronologie. John F. W. Herschel then developed them for astronomical use in his 1849 Outlines of Astronomy, after acknowledging that Ideler was his guide.

The period thus arising of 7980 Julian years, is called the Julian period, and it has been found so useful, that the most competent authorities have not hesitated to declare that, through its employment, light and order were first introduced into chronology. We owe its invention or revival to Joseph Scaliger, who is said to have received it from the Greeks of Constantinople. The first year of the current Julian period, or that of which the number in each of the three subordinate cycles is 1, was the year 4713 BC, and the noon of 1 January of that year, for the meridian of Alexandria, is the chronological epoch, to which all historical eras are most readily and intelligibly referred, by computing the number of integer days intervening between that epoch and the noon (for Alexandria) of the day, which is reckoned to be the first of the particular era in question. The meridian of Alexandria is chosen as that to which Ptolemy refers the commencement of the era of Nabonassar, the basis of all his calculations.
At least one mathematical astronomer adopted Herschel's "days of the Julian period" immediately. Benjamin Peirce of Harvard University used over 2,800 Julian days in his Tables of the Moon, begun in 1849 but not published until 1853, to calculate the lunar ephemerides in the new American Ephemeris and Nautical Almanac from 1855 to 1888. The days are specified for "Washington mean noon", with Greenwich defined as 18h 51m 48s west of Washington (282°57′W, or Washington 77°3′W of Greenwich). A table with 197 Julian days ("Date in Mean Solar Days", one per century mostly) was included for the years –4713 to 2000 with no year 0, thus "–" means BC, including decimal fractions for hours, minutes, and seconds. The same table appears in Tables of Mercury by Joseph Winlock, without any other Julian days.
The national ephemerides started to include a multi-year table of Julian days, under various names, for either every year or every leap year beginning with the French Connaissance des Temps in 1870 for 2,620 years, increasing in 1899 to 3,000 years. The British Nautical Almanac began in 1879 with 2,000 years. The Berliner Astronomisches Jahrbuch began in 1899 with 2,000 years. The American Ephemeris was the last to add a multi-year table, in 1925 with 2,000 years. However, it was the first to include any mention of Julian days with one for the year of issue beginning in 1855, as well as later scattered sections with many days in the year of issue. It was also the first to use the name "Julian day number" in 1918. The Nautical Almanac began in 1866 to include a Julian day for every day in the year of issue. The Connaissance des Temps began in 1871 to include a Julian day for every day in the year of issue.
The French mathematician and astronomer Pierre-Simon Laplace first expressed the time of day as a decimal fraction added to calendar dates in his book, Traité de Mécanique Céleste, in 1823. Other astronomers added fractions of the day to the Julian day number to create Julian Dates, which are typically used by astronomers to date astronomical observations, thus eliminating the complications resulting from using standard calendar periods like eras, years, or months. They were first introduced into variable star work in 1860 by the English astronomer Norman Pogson, which he stated was at the suggestion of John Herschel. They were popularized for variable stars by Edward Charles Pickering, of the Harvard College Observatory, in 1890.
Julian days begin at noon because when Herschel recommended them, the astronomical day began at noon. The astronomical day had begun at noon ever since Ptolemy chose to begin the days for his astronomical observations at noon. He chose noon because the transit of the Sun across the observer's meridian occurs at the same apparent time every day of the year, unlike sunrise or sunset, which vary by several hours. Midnight was not even considered because it could not be accurately determined using water clocks. Nevertheless, he double-dated most nighttime observations with both Egyptian days beginning at sunrise and Babylonian days beginning at sunset. Medieval Muslim astronomers used days beginning at sunset, so astronomical days beginning at noon did produce a single date for an entire night. Later medieval European astronomers used Roman days beginning at midnight so astronomical days beginning at noon also allow observations during an entire night to use a single date. When all astronomers decided to start their astronomical days at midnight to conform to the beginning of the civil day, on 1 January 1925, it was decided to keep Julian days continuous with previous practice, beginning at noon.
During this period, usage of Julian day numbers as a neutral intermediary when converting a date in one calendar into a date in another calendar also occurred. An isolated use was by Ebenezer Burgess in his 1860 translation of the Surya Siddhanta wherein he stated that the beginning of the Kali Yuga era occurred at midnight at the meridian of Ujjain at the end of the 588,465th day and the beginning of the 588,466th day (civil reckoning) of the Julian Period, or between 17 and 18 February JP 1612 or 3102 BC. Robert Schram was notable beginning with his 1882 Hilfstafeln für Chronologie. Here he used about 5,370 "days of the Julian Period". He greatly expanded his usage of Julian days in his 1908 Kalendariographische und Chronologische Tafeln containing over 530,000 Julian days, one for the zeroth day of every month over thousands of years in many calendars. He included over 25,000 negative Julian days, given in a positive form by adding 10,000,000 to each. He called them "day of the Julian Period", "Julian day", or simply "day" in his discussion, but no name was used in the tables. Continuing this tradition, in his book "Mapping Time: The Calendar and Its History" British physics educator and programmer Edward Graham Richards uses Julian day numbers to convert dates from one calendar into another using algorithms rather than tables.


== Julian day number calculation ==
The Julian day number can be calculated using the following formulas (integer division rounding towards zero is used exclusively, that is, positive values are rounded down and negative values are rounded up):
The months January to December are numbered 1 to 12. For the year, astronomical year numbering is used, thus 1 BC is 0, 2 BC is −1, and 4713 BC is −4712. JDN is the Julian Day Number. Use the previous day of the month if trying to find the JDN of an instant before midday UT.


=== Converting Gregorian calendar date to Julian day number ===
The algorithm is valid for all (possibly proleptic) Gregorian calendar dates after 23 November −4713. Divisions are integer divisions towards zero; fractional parts are ignored.
JDN=1461⋅(Y+4800+M−1412)4+367⋅(M−2−12⋅M−1412)12−3⋅Y+4900+M−14121004+D−32075


=== Converting Julian calendar date to Julian day number ===
The algorithm is valid for all (possibly proleptic) Julian calendar years ≥ −4712, that is, for all JDN ≥ 0. Divisions are integer divisions, fractional parts are ignored.


=== Finding Julian date given Julian day number and time of day ===
For the full Julian Date of a moment after 12:00 UT one can use the following. Divisions are real numbers.

So, for example, 1 January 2000, at 18:00:00 UT corresponds to JD = 2451545.25 and 1 January 2000, at 6:00:00 UT corresponds to JD = 2451544.75.


=== Finding day of week given Julian day number ===
Because a Julian day starts at noon while a civil day starts at midnight, the Julian day number needs to be adjusted to find the day of week: for a point in time in a given Julian day after midnight UT and before 12:00 UT, add 1 or use the JDN of the next afternoon.
The US day of the week W1 (for an afternoon or evening UT) can be determined from the Julian Day Number J with the expression:

If the moment in time is after midnight UT (and before 12:00 UT), then one is already in the next day of the week.
The ISO day of the week W0 can be determined from the Julian Day Number J with the expression:


=== Julian or Gregorian calendar from Julian day number ===
This is an algorithm by Edward Graham Richards to convert a Julian Day Number, J, to a date in the Gregorian calendar (proleptic, when applicable). Richards states the algorithm is valid for Julian day numbers greater than or equal to 0. All variables are integer values, and the notation "a div b" indicates integer division, and "mod(a, b)" denotes the modulus operator.

For Julian calendar:

f = J + j
For Gregorian calendar:

f = J + j + (((4 × J + B) div 146097) × 3) div 4 + C
For Julian or Gregorian, continue:

D, M, and Y are the numbers of the day, month, and year respectively for the afternoon at the beginning of the given Julian day.


=== Julian period from indiction, Metonic and solar cycles ===
Let Y be the year BC or AD and i, m, and s respectively its positions in the indiction, Metonic and solar cycles. Divide 6916i + 4200m + 4845s by 7980 and call the remainder r.

Example
i = 8, m = 2, s = 8. What is the year?


== Julian date calculation ==
As stated above, the Julian date (JD) of any instant is the Julian day number for the preceding noon in Universal Time plus the fraction of the day since that instant. Ordinarily calculating the fractional portion of the JD is straightforward; the number of seconds that have elapsed in the day divided by the number of seconds in a day, 86,400. But if the UTC timescale is being used, a day containing a positive leap second contains 86,401 seconds (or in the unlikely event of a negative leap second, 86,399 seconds). One authoritative source, the Standards of Fundamental Astronomy (SOFA), deals with this issue by treating days containing a leap second as having a different length (86,401 or 86,399 seconds, as required). SOFA refers to the result of such a calculation as "quasi-JD".


== See also ==


== Notes ==


== References ==


== Sources ==


== External links ==
"Julian Date Converter". US Naval Observatory. Retrieved 30 August 2023.
