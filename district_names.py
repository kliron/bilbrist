district_names = {
    '193': ['Hersby', 'Herserud', 'Islinge', 'Torsvik', 'Grönsta', 'Näset', 'Sticklinge'],
    '194': ['Baggeby', 'Gångsätra', 'Lidingö Sjukhus', 'Larsberg', 'Skärsätra', 'Stockby'],
    '195': ['Bo', 'Bosön', 'Elfvik', 'Rudboda'],
    '196': ['Brevik', 'Ekholmsnäs', 'Gashaga', 'Högberga kursgård', 'Killinge', 'Käppala'],
    '201': ['Traneberg', 'Ulvsunda'],
    '202': ['Smedslätten', 'Stora mossen', 'Appelviken'],
    '203': ['Höglandet', 'Nockeby', 'Nockebyhov', 'Olovslund', 'Alsten'],
    '204': ['Abrahamsberg', 'Riksby', 'Äkeshov', 'Akeslund'],
    '205': ['Mariehäll', 'Ulvsunda industriom'],
    '206': ['Bromma flygplats'],
    '211': ['Drottningholm', 'Lovön'],
    '212': ['Ska', 'Stenhamra', 'Sanga Säby'],
    '213': ['Färingsö', 'Färentuna', 'Hilleshög'],
    '214': ['Tappström', 'Träkvista', 'Älvnäs'],
    '215': ['Ekerön', 'Skytteholms kursgård', 'Ekerö Sommarstad'],
    '216': ['Munsön'],
    '217': ['Adelsö'],
    '221': ['Beckomberga', 'Blackeberg', 'Bromma kyrka', 'Norra Ängby', 'Södra Ängby'],
    '222': ['Bällsta', 'Flysta', 'Solvalla', 'Sundby'],
    '223': ['Grimsta', 'Rácksta', 'Vällingby'],
    '231': ['Lunda', 'Nälsta', 'Solhem', 'Spånga Centrum'],
    '232': ['Kälvesta', 'Vinsta'],
    '233': ['Hässelby gård', 'Hässelby strand'],
    '234': ['Backlura', 'Hässelby villastad'],
    '241': ['Bromsten'],
    '242': ['Rinkeby', 'Hjulsta', 'Tensta'],
    '251': ['Barkarby', 'Skälby', 'Veddesta'],
    '252': ['Viksjö'],
    '253': ['Jakobsberg'],
    '254': ['Almare kursgård', 'Kalhäll', 'Stäket'],
    '255': ['Kungsängen'],
    '256': ['Brunna', 'Gällöfsta kursgård'],
    '257': ['Bro', 'Lejondals slott', 'Tammsvik kursgård', 'Tibble'],
    '258': ['Aske kursgård'],
    '259': ['Skokloster'],
    '260': ['Aronsborgs kursgård', 'Bálsta', 'Balsta Gästis kursgård', 'Krägga herrgård', 'Lastbergets kursgård', 'Thoresta herrgård'],
    '261': ['Fagerudds kursgård', 'Fribergs herrgård', 'Strömsbergs säteri'],
    '301': ['Haga', 'Karolinska sjukhus'],
    '302': ['Huvudsta'],
    '303': ['Skytteholm', 'Solna Centrum'],
    '305': ['Hagalund', 'Råsunda', 'Haga'],
    '304': ['Solna Buisness Park'],
    '306': ['Frösunda'],
    '307': ['Frösundavik Stolpe'],
    '308': ['Bergshamra', 'Jäva', 'Ulriksdal'],
    '312': ['Sundbyberg'],
    '313': ['Duvbo', 'Hallonbergen', 'Rissne'],
    '314': ['Ursvik'],
    '331': ['Kista', 'Akalla', 'Husby'],
    '333': ['Edsviken', 'Helenelund', 'Tegelhagen'],
    '334': ['Häggvik', 'Tureberg'],
    '335': ['Bergendals kursgård', 'Edsberg', 'Sjöberg'],
    '336': ['Norrviken', 'Rotebro', 'Viby'],
    '346': ['Bollstanäs', 'Bredden'],
    '347': ['Upplands Väsby'],
    '348': ['Löwenströmska'],
    '351': ['Rosersberg'],
    '353': ['Märsta/Arlandastad', 'Steningevik kursgård'],
    '354': ['Sigtuna', 'Sigtuna Norr'],
    '362': ['Arlandaområdet'],
    '363': ['Arlanda Remoten'],
    '364': ['Arlanda inom Flygplatsen'],
    '366': ['Odensala'],
    '367': ['Skepptuna'],
    '368': ['Knivsta', 'Krusenbergs herrgård'],
    '369': ['Almunge'],
    '371': ['Uppsala Centrum'],
    '401': ['Frescati', 'Norra Djurgården', 'Universitetet'],
    '402': ['Djursholm', 'Mörby', 'Stocksund', 'Svalnäs', 'Klingsta', 'Nora'],
    '411': ['Enebyberg', 'Roslags Näsby', 'Skarpäng'],
    '412': ['Näsby Park', 'Hägernäs', 'Viggbyholm'],
    '413': ['Ensta', 'Täby Centrum', 'Laháll', 'Gribbylund', 'Visinge'],
    '421': ['Arninge', 'Skávsjöholms kursgård', 'Svinninge'],
    '416': ['Såstaholm kursgård', 'Täby Kyrkby'],
    '417': ['Lindholmen', 'Vallentuna'],
    '418': ['Frösunda'],
    '419': ['Kårsta', 'Brottby'],
    '422': ['Rydbo', 'Vaxholm'],
    '424': ['Täljöviken kursgård', 'Akers Runö', 'Akersberga', 'Osterskär'],
    '425': ['Skärgárdsstad'],
    '426': ['Roslagskula'],
    '427': ['Ljusterö'],
    '501': ['Rádmansö'],
    '502': ['Furusund'],
    '503': ['Blido'],
    '504': ['Högmarsö'],
    '505': ['Riala'],
    '506': ['Norrtälje'],
    '507': ['Vätö'],
    '508': ['Roslagsbro'],
    '509': ['Söderby Karl'],
    '510': ['Väddö Södra'],
    '511': ['Älmsta'],
    '512': ['Väddö Norra'],
    '513': ['Hallstavik'],
    '514': ['Edsbro'],
    '515': ['Rimbo', 'Ranäs Slott', 'Johannesbergs slott'],
    '516': ['Husby/Sjuhundra'],
    '601': ['Hammarby sjöstad', 'Henriksdal', 'Kvarnholmen'],
    '602': ['Finntorp', 'Hästhagen', 'Järla', 'Sickla'],
    '603': ['Augustendal', 'Jarlaberg', 'Lillängen', 'Nacka Strand', 'Storängen', 'Vikdalen'],
    '604': ['Duvnäs', 'Duvnäs utskog', 'Ektorp', 'Skuru'],
    '605': ['Eknäs', 'Lännersta'],
    '606': ['Björknäs', 'Eriksviks kursgård', 'Hasseluddens kursgård', 'Orminge', 'Skepparholmens kursgård'],
    '607': ['Kummelnäs', 'Vikingshill'],
    '611': ['Baggensudden', 'Fisksätra', 'lgelboda', 'Ljuskärrsberget', 'Neglinge', 'Tattby'],
    '612': ['Rösunda', 'Solsidan', 'Vår Gard kursgård', 'Algo'],
    '631': ['Grisslinge', 'Gustavsberg', 'Skeviks kursgård'],
    '632': ['Ingaro', 'Ingaröstrand', 'Kalkarsveden', 'Klacknäset', 'Ramsdalen', 'Skälsmara', 'Säby Säteri', 'Tranarö'],
    '633': ['Tynningö'],
    '641': ['Hemmesta', 'Kalvandö', 'Norrnäs', 'Skeppsdalsström', 'Sodernäs', 'Strömma', 'Torsby', 'Angsvik'],
    '642': ['Boda', 'Edslösa', 'Kalvsvik', 'Lillsved', 'Löknäs', 'Myttinge', 'Norräva', 'Skägga', 'Skärmaräng', 'Stenslätten', 'Sund'],
    '643': ['Saltarö'],
    '644': ['Fågelbro', 'Fågelbrolandet', 'Hässelmara', 'Lillströmsudd', 'Malma', 'Malmaön', 'Stavsnäs'],
    '645': ['Djuro', 'Sollenkroka', 'Vindö', 'Överby'],
    '701': ['Hammarby sjöstad', 'Södra Hammarbyhamnen'],
    '702': ['Hammarbyhöjden', 'Johanneshov'],
    '704': ['Björkhagen', 'Enskededalen', 'Gamla Enskede', 'Kärrtorp', 'Bagarmossen'],
    '711': ['Skarpnäck'],
    '713': ['Sköndal'],
    '714': ['Älta'],
    '715': ['Fornudden', 'Trollbäcken'],
    '716': ['Bollmora'],
    '717': ['Krusboda', 'Lindalen', 'Oringe', 'Tyresö strand'],
    '718': ['Raksta'],
    '719': ['Brevik', 'Gamla Tyresö'],
    '721': ['Gubbängen', 'Tallkrogen'],
    '722': ['Fagersjö', 'Hökarängen'],
    '723': ['Farsta'],
    '724': ['Agesta'],
    '726': ['Vidja'],
    '731': ['Skogas', 'Stortorp', 'Trángsund'],
    '732': ['Länna', 'Vega'],
    '733': ['Kolartorp'],
    '734': ['Handen'],
    '735': ['Brandbergen'],
    '736': ['Vendelsö'],
    '737': ['Tutviken'],
    '741': ['Jordbro'],
    '742': ['Västerhaninge'],
    '746': ['Arsta havsbad'],
    '747': ['Tungelsta'],
    '748': ['Almåsa kursgård', 'Häringe slott'],
    '749': ['Hemfosa'],
    '751': ['Ösmo'],
    '752': ['Muskö'],
    '753': ['Sorunda'],
    '754': ['Nynäshamn'],
    '755': ['Torö'],
    '756': ['Lisö'],
    '766': ['Osterhaninge'],
    '767': ['Ava'],
    '768': ['Gàlö'],
    '769': ['Dalarö', 'Smadalarö kursgård'],
    '801': ['Arsta'],
    '802': ['Globen'],
    '803': ['Enskede gård', 'Enskedefältet', 'Gamla Enskede'],
    '811': ['Liseberg', 'Orby slott', 'Ostberga'],
    '812': ['Stureby', 'Svedmyra', 'Bandhagen'],
    '813': ['Högdalen', 'Orby'],
    '814': ['Hagsätra', 'Rágsved'],
    '815': ['Langbro', 'Älvsjö', 'Fruängen', 'Herrängen', 'Langsjö'],
    '821': ['Stuvsta'],
    '822': ['Myrängen'],
    '823': ['Snättringge'],
    '831': ['Fullersta'],
    '832': ['Huddinge Centrum', 'Sjödalen'],
    '833': ['Gladökvarn', 'Lissma'],
    '834': ['Glömsta'],
    '835': ['Flemingsberg', 'Huddinge sjukhus'],
    '841': ['Tullinge'],
    '842': ['Norra Tumba', 'Uttran'],
    '843': ['Södra Tumba'],
    '844': ['Vårsta'],
    '901': ['Gröndal', 'Liljeholmen'],
    '902': ['Aspudden', 'Midsommarkransen'],
    '905': ['Solberga', 'Västberga'],
    '911': ['Hägerstensåsen', 'Västertorp'],
    '912': ['Mälarhöjden'],
    '913': ['Bredäng', 'Sätra'],
    '922': ['Kungens kurva', 'Segeltorp'],
    '923': ['Skärholmen', 'Vårberg', 'Vårby'],
    '931': ['Alby', 'Fittfa', 'Masmo'],
    '932': ['Eriksberg', 'Hallunda', 'Norsborg'],
    '941': ['Rönninge', 'Salem'],
    '942': ['Ladviks kursgård', 'Viksber'],
    '943': ['Brunnsäng', 'Ekensberg', 'Skogshöjd'],
    '944': ['Ostertälje'],
    '945': ['Barsta', 'Mariekälla', 'Saltskog', 'Södertälje Centrum'],
    '946': ['Hovsjö', 'Linahage', '|Ronna', 'Västertälje'],
    '951': ['Enhörna'],
    '952': ['Nykvarn', 'Bommersvik'],
    '953': ['Järna'],
    '954': ['Hölö', 'Mörkö'],
    '955': ['Gnesta', 'Mölnbo'],
    '956': ['Skavsta flygplats/Nyköping'],
    '101': ['Gamla Stan'],
    '111': ['Slussen'],
    '112': ['Viking Line terminalen'],
    '113': ['Skanstull'],
    '121': ['Mariatorget'],
    '122': ['Södra station'],
    '123': ['Rosenlund'],
    '124': ['Hornstull'],
    '125': ['Södersjukhuset'],
    '131': ['Kungliga Operan'],
    '132': ['Hötorget'],
    '134': ['Gallerian'],
    '135': ['Grand Hotel Sthlm'],
    '136': ['Centralstationen'],
    '141': ['S:t Eriks Ögonsjukhus'],
    '142': ['Fridhemsplan'],
    '143': ['Trossen'],
    '151': ['S:t Görans Sjukhus'],
    '152': ['Kristineberg'],
    '153': ['Fredhäll'],
    '154': ['Dagens Nyheter'],
    '155': ['Lilla stora Essingen'],
    '161': ['Sabbatsberg'],
    '162': ['S:t Eriksplan'],
    '163': ['Norrtull'],
    '164': ['Odenplan'],
    '165': ['Roslagstull'],
    '166': ['Mc Donalds Sveavägen'],
    '167': ['Engelbrekt'],
    '168': ['Tekniska Högskolan'],
    '181': ['Stureplan'],
    '182': ['Historiska Museet'],
    '184': ['Ostra Reals Gymnasium'],
    '185': ['Gardet'],
    '186': ['Radiohuset'],
    '187': ['DJurgárdsslätten Skansen'],
    '188': ['Tekniska Museet'],
    '191': ['Färjeterminaler Silja Line/Talink'],
    '192': ['Stora Skuggan'],
}
