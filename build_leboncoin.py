#!/usr/bin/env python3
"""Build leboncoin.json from scraped data."""
import json

IMG = "https://img.leboncoin.fr/api/v1/lbcpb1/images/"
URL = "https://www.leboncoin.fr/ad/chaussures/"

RAW = """JM Weston 180 mocassins cuir crocodile / caïman marron taille 7C§1660§Fort-de-France§40§Très bon état§3157242322§58/f5/40/58f5408c3e16bfecfc98b2a878f4ab988b1c2b05.jpg§2026-03-07 16:00:45
Mocassins 180 JM Weston marron 41§155§Toulouse§41§Très bon état§3170280113§5a/50/59/5a5059036f205492e211302f52a4977154708743.jpg§2026-03-29 14:24:04
Mocassins 180 J.M. Weston§200§Athis-Mons§42§§3165910248§42/79/e5/4279e5cf5173e8e5c3ec7031d6f27717e6b8b734.jpg§2026-03-21 23:23:42
Mocassins 180 J.M. Weston§220§Athis-Mons§41§§3165909690§5f/b6/d8/5fb6d8650f80d3688cf6018fc388ea5983ca622a.jpg§2026-03-21 23:20:32
Chaussure MOCASSIN 180 J.M WESTON§250§Saucats§44§Très bon état§3106439765§06/4c/8b/064c8b95a3671929914c2e80a13b7cdc9bf8e416.jpg§2025-12-05 15:11:57
Mocassins 180 JM Weston Bleu Marine - 7.E - T 41§292§Paris§41§Très bon état§3170730577§94/77/e3/9477e3ea3923df842126417042ae94825fa267a1.jpg§2026-03-30 07:31:41
J.M. Weston Mocassins 180 – Marron Mélèze – 9D§780§Paris§44§Très bon état§3162047961§5f/79/ec/5f79eca040a4e72e398a1d8d1001534b1eadacbc.jpg§2026-03-15 10:42:06
J.M. Weston 180 Mocassin - Bordeaux - Taille 6/E (41 Wide)§220§Paris§41§Très bon état§3168418506§ab/3e/97/ab3e97b09ceb76056f39d1f79c57947b42b945eb.jpg§2026-03-26 10:22:26
Mocassins 180 JM Weston Noir - 8/5 D - T 42/5§313§Paris§42,5§Très bon état§3160248689§ae/6a/f3/ae6af32a75092d96984c271f540593f7b2a30989.jpg§2026-03-12 06:47:57
Mocassins 180 JM Weston Homme Cuir Noir Semelle Gomme 6C – 40FR 🇫🇷§240§Lille§40§Très bon état§3165416217§ac/11/c4/ac11c4a00e396679c1f840817f2a1e18734c026f.jpg§2026-03-21 09:39:04
J.M Weston 180§170§Paris§42§Bon état§3144501004§58/c0/a9/58c0a978e0031bb1586f8409dd4b71fcc2aac3ab.jpg§2026-02-13 19:23:47
👞Mocassins vintage J.M. Weston 180 👞§950§Saint-Germain-en-Laye§41§Très bon état§3156612865§55/0f/b3/550fb35dc8207d94dd6e2adf9ecddd752e6e3d1c.jpg§2026-03-06 22:24:25
Mocassins 180 JM Weston Bi Matière Cuir & Daim Toucan - 7/5 D - T 41/5§444§Paris§41,5§Très bon état§3170293726§7f/ad/6e/7fad6e46ccc6be44f493b6bdec8c653a9256fe65.jpg§2026-03-29 14:41:17
Mocassins 180 JM Weston Cuir Noir 8,5C – 43FR 🇫🇷§280§Lille§43§Très bon état§3156862673§bb/59/fb/bb59fba50b3ac9528b3d1c75cb0885417cd85687.jpg§2026-03-07 10:38:15
J.M. Weston mocassin 180 en cuir lisse noir, taille 5E (38), état neuf, jamais portés§550§Paris§38§Neuf sans étiquette§3169930404§31/9a/1c/319a1c07e4e70a96865ce5984a7be388d2abb9e2.jpg§2026-03-28 19:18:59
Mocassins Ladies 180 JM Weston - Daim marron Mélèze - 4/5 C - T 37/5§303§Paris§37,5§Très bon état§3159839791§e4/d0/8b/e4d08bb4394879147dde707018b99f49578b6a93.jpg§2026-03-11 12:11:09
J.M Weston moccasin grainé 180§220§Villepinte§40§Très bon état§3137306379§7a/82/dc/7a82dc0f07e79ec3055fd50cbdae7f83b6ca9836.jpg§2026-01-31 22:27:41
J.M. Weston Mocassins 180 - Boxcalf Noir - UK 10 / US 11 D (Très bon état)§490§La Celle-Saint-Cloud§44,5§Très bon état§3165083391§ac/3a/86/ac3a86c33dbc6d56113f4e215b92e29afdd83361.jpg§2026-03-20 15:46:50
Mocassins JM. Weston§350§Paris§41,5§Très bon état§3164034235§0e/7e/84/0e7e840f1ddc6374f6e1bf8d18b6db0922527ee2.jpg§2026-03-18 15:58:53
JM WESTON 180 mocassins semelles neuves taille 6,5 E / 40,5 large cuir marron penny loafers chaussures§349§Paris§40,5§Très bon état§3127857090§db/af/d3/dbafd33c39156fd8a7bc3590468d6833d811351a.jpg§2026-01-14 21:43:55
Mocassins 180 JM Weston Box Calf Noir 6,5D – 41FR 🇫🇷§380§Lille§41§Très bon état§3144835047§7f/90/65/7f906513a76b48fa4d331f9dff24559fca2a7e71.jpg§2026-02-14 13:54:48
Mocassin WESTON 180§175§Chambourcy§41,5§État satisfaisant§3142770353§97/68/cf/9768cf932a697866f1932efc5f24ef956a9bd1ed.jpg§2026-02-10 14:16:01
Mocassins JM Weston§250§Paris§39,5§Très bon état§3123073989§18/8c/72/188c725f753008a5e9c0f0985b08d073fee4e8c3.jpg§2026-01-05 19:28:23
JM Weston 180§399§Clichy§41,5§Bon état§3003649491§ff/06/69/ff06690b77d2483c7b2353c746a1220a28bac8e5.jpg§2025-06-08 11:05:28
Jm.weston§400§Saint-Étienne§40,5§Bon état§3129959290§1d/7b/10/1d7b1014861d8dc7bcdd00d6cb08f9bd6fd93b43.jpg§2026-01-18 17:14:53
Mocassin 180 J.M. Weston cuir noir§169§Sainte-Geneviève-des-Bois§41,5§Bon état§3130200252§66/ef/9a/66ef9aeb0dc0a860d18f4163b66adac2c6514d0e.jpg§2026-01-19 01:56:44
Mocassin Weston 180 - 500§450§Paris§43§Très bon état§3053245055§58/33/c3/5833c3281cf29df9f1166aef9292b74943fe3d9c.jpg§2025-09-07 20:33:29
Jm weston§260§Plaisir§43,5§Bon état§3073472420§25/a5/9f/25a59f17040af0e867ac5d70e70aab5afed54162.jpg§2025-10-12 15:15:34
Jm weston moc 180§530§Levallois-Perret§45§Très bon état§2324738522§c0/e3/9a/c0e39a41ae8d96602a31eda39f44e97cdc442fd8.jpg§2023-03-30 14:17:34
J.M Weston 180§180§Paris§41§Bon état§3144502101§96/64/f7/9664f7e06466241f06f9cec58e1f810f12b82536.jpg§2026-02-13 19:25:54
Mocassins JM. Weston§190§Paris§39§État satisfaisant§3121951925§48/fb/88/48fb884c9c0d222decc1d9944a6733d0219d8e65.jpg§2026-01-03 23:26:27
Mocassin JM Weston marron occasion§350§Orléans§42§Bon état§2909870673§e4/04/26/e404264dab9040a112a8717c3ceaf2032526b431.jpg§2024-12-28 19:21:58
J.m. Weston originale chaussures§250§Pornichet§42§Très bon état§2999988760§fb/9a/a9/fb9aa93c8ed5d2e768195e8fb0f210ad3a399362.jpg§2025-06-01 21:16:07
Mocassin JM Weston 40,5§249§Lagny-sur-Marne§40,5§Bon état§3097706564§36/b0/a5/36b0a5ab77f0a4236a17556cbeb03bd455111c5f.jpg§2025-11-20 17:14:56
Mocassins JM Weston modèle 180 pointure 6D§150§Puget-sur-Argens§40§Bon état§3124583440§f3/20/b9/f320b91098bb418f48a2d4fa10761ba8f1cc97e5.jpg§2026-01-08 20:15:48
Mocassins Penny Loafer Paraboot marron 41§140§Toulouse§41§Très bon état§3171348880§51/ea/91/51ea9151b17f52bbcba7f8c76c7bcfada4b48790.jpg§2026-03-31 10:26:32
Mocassins JM Weston Marron Bergeronette - 6/5 D - T 40/5§280§Paris§40,5§Très bon état§3140746561§c8/60/5a/c8605ab46f7adf1a0a69a948ab7423b125d795e4.jpg§2026-02-07 08:28:39
Mocassins JM. Weston§350§Paris§41§Très bon état§3137361854§82/77/8d/82778d2168dc0fe47ec73262625fd9b806668071.jpg§2026-02-01 08:07:06
Mocassins JM. Weston§290§Paris§39,5§Très bon état§3137365366§46/96/0e/46960e5fd4479d720fae04c5d714a7f0e7cd34c8.jpg§2026-02-01 08:22:23
Mocassins J.M. Weston 180 et embauchoirs§150§Paray-Vieille-Poste§40§Bon état§3113047174§f1/b7/b8/f1b7b8cdad18b7e7dd478d749cf74cd13c47676d.jpg§2025-12-15 18:40:50
Mocassins JM. Weston§290§Paris§41,5§Très bon état§3137360524§5c/18/e1/5c18e1abc4aba53a9d69cc0d478aad6e8bf57fa6.jpg§2026-02-01 08:00:40
J.M. Weston mocassin 180 femme taille 3/E§295§Paris§38§Très bon état§3113426000§f0/33/d0/f033d0d0d77033fff79dbf6f075e7babadd6a9c6.jpg§2025-12-16 14:46:09
Mocassin JM Weston 39§249§Lagny-sur-Marne§39§Très bon état§3131431546§52/58/fe/5258fe075f130eb53867ff73be4f478ed91b7ff7.jpg§2026-01-21 12:51:20
Mocassin JM Weston 40§190§Lagny-sur-Marne§40§Bon état§3131106792§77/69/45/776945a9aac6abc7453cf3967be5e3027e3b0f06.jpg§2026-01-20 17:57:43
Mocassins JM Weston§590§Dijon§43,5§Très bon état§3128740255§21/1d/8d/211d8d7a53c0aaa1ac72c5baa495bae4c0cee068.jpg§2026-01-16 17:30:44
Mocassin J.M.Weston 180 Commando§350§Sarcelles§40§Très bon état§3126270134§bf/5e/51/bf5e511ad32d2718e50cce5b33f7c2688ee8911d.jpg§2026-01-11 20:13:54
Mocassins JM. Weston§350§Paris§41§Très bon état§3127328564§e2/00/15/e20015e361292066c8c1b1cb33800a6e67059daa.jpg§2026-01-13 20:31:55
Mocassins JM. Weston§250§Paris§38§Bon état§3126813234§5b/8a/71/5b8a717d783828f02e017a53b7efda6b90d61cd3.jpg§2026-01-12 20:31:03
MOCASSINS JM WESTON Modèle 180 à Rénover pointure 39 ( Pointure UK 5/E Pointure US 7 En )§70§Sotteville-lès-Rouen§39§Bon état§3102351670§8b/c0/9e/8bc09e6d7588656c821838a1ff1260a50e7df3f9.jpg§2025-11-28 16:21:09
Chaussures J. WESTON Homme T40§330§Félines§40§Bon état§3114832364§9a/10/bb/9a10bbb933c903bb30c8277bf107953fdda469bc.jpg§2025-12-19 13:34:04
Mocassins J.M. Weston 7133 Noir – 7E (41) - Excellent état§220§Paris§41§Très bon état§3112291963§df/37/d8/df37d84404cec88becbc9394b8ea7b8bd53d0eaf.jpg§2025-12-14 14:03:11
Weston J. M. Belle ceinture en box marron bergeronnette taille 90 plus pairede gants en cuir§180§Courbevoie§§Très bon état§3111929800§9a/e3/e9/9ae3e9241ac2eaeeab841871dd657b2dbe6181c4.jpg§2025-12-13 19:20:04
Mocassins emblématiques JM Weston ref 180 marron vintage§150§Le Vésinet§43§État satisfaisant§3165974394§41/fc/12/41fc12a18da0ffda2daae7c8fe8f51a3fbeee7da.jpg§2026-03-22 08:58:23
Mocassins J.M. Weston 180 bergeronnette§349§Sainte-Geneviève-des-Bois§42§Très bon état§3143105583§e3/6c/de/e36cdeee25f98ce5f561fa26404e0157fe6cf764.jpg§2026-02-11 08:04:18
Mocassins 180 JM Weston Bleu Marine - 7.E - T 41§313§Paris§41§Très bon état§3169977079§bf/bd/1c/bfbd1c256ffbbfcab1928ed469295a4eb325427c.jpg§2026-03-28 20:57:08
Mocassin JM Weston 180 noir grainé 6.5 E (40) semelles neuves§205§Garches§40§Très bon état§3079994677§76/09/48/760948a05f5713a6f60a58b04cc1a2fc64b74c23.jpg§2025-10-23 20:28:46
Chaussure J.M Weston Mocassin 180§500§Argenteuil§45§Très bon état§3055812163§59/21/66/592166a9c7ce23060ccfdd586b5aa33cbdb91a3e.jpg§2025-09-11 19:39:17
Mocassins 180 J.M. Weston Cuir Noir 8,5C – 43FR 🇫🇷§230§Lille§43§Très bon état§3161373198§2f/41/d6/2f41d6cfc15200ac4fadb62ddaf7236916be24b1.jpg§2026-03-14 09:55:56
Mocassins 180 JM Weston Cuir Noir 6,5D – 41FR 🇫🇷§280§Lille§41§Très bon état§3156872939§ce/38/09/ce380994812af46546625ba13fe3662cc272c650.jpg§2026-03-07 10:45:03
Mocassins 180 J.M Weston taille 41§300§Angoulême§41§Très bon état§3072817237§c5/b9/55/c5b9551ac5925568b9845625fab57eac7a283dee.jpg§2025-10-11 13:46:06
Mocassins JM WESTON 7,5 C Velours Camel§550§Fontenay-sous-Bois§41,5§Très bon état§3079115595§dc/f2/e0/dcf2e009e5ffdfa276fd1eddf21eb9584f1ed06f.jpg§2025-10-22 12:54:12
Mocassin J.M Weston§450§La Queue-en-Brie§35§Très bon état§3076856935§ae/2d/e9/ae2de934200b800df81ffc84a93ad2b95c013cb9.jpg§2025-10-18 16:25:11
Weston mocassins Taille 7 1/2 B§400§Maisons-Alfort§41,5§Très bon état§3065130289§55/2a/5e/552a5e79bd9750722b17ceeaf6cd889395eb74a1.jpg§2025-09-27 17:30:04
Richelieu JM Weston 7UK E homme bordeaux§100§Paris§42§État satisfaisant§2320069483§22/50/76/22507642aec8c6a027a43984c586436e1ed8d55b.jpg§2023-03-21 16:32:54
Mocassin JM Weston modèle 180 cuir noir veau grainé.Excellent état§340§Avon§40§Très bon état§2312407700§50/f0/dc/50f0dc1204c5254042ad3f1e56ba926d420312ff.jpg§2023-03-08 15:19:27
Vends mocassins J.M.WESTON§290§Lanton§43§Bon état§2302754828§11/b7/fc/11b7fc69cb5545ee344f1ab95c583d9ccad9d3e9.jpg§2023-02-18 13:56:31
JM Weston femme taille 36 1/2 TBE§100§Rueil-Malmaison§36§Très bon état§2274071209§4b/03/af/4b03af23342471b7ca5c563446d8a41d817fdb0c.jpg§2022-12-21 13:35:57
Mocassins weston 8B veau velours noir§350§Paris§42§Très bon état§2256715170§c4/da/5a/c4da5a235d21701110a5e1feba06578528f2cc0c.jpg§2022-11-19 12:55:47
Mocassin 180 de JM Weston§200§Jonzac§41§Très bon état§2222112847§77/d7/e3/77d7e3c93e54cefdd975b12d38d667ffbcad25f7.jpg§2022-09-16 04:05:30
Mocassins 180 - JM WESTON§290§Bort-les-Orgues§42§Bon état§2124493387§24/e7/76/24e776dadbceaffd78113e3d7513616656bb0f44.jpg§2022-03-01 13:10:47
Mocassin JM Weston modèle 180 cuir veau box taille 8 D excellent état§550§Paris§42§Très bon état§2086414551§98/43/b7/9843b747ae5e0c5a62a858368ecf8256b50369aa.jpg§2021-12-11 17:25:51
Chaussures J.M. Weston 180 Mocassin§200§Paris§36§Très bon état§2071595933§a4/f6/4f/a4f64f2e2390655242cff585ac943e9a446d76a7.jpg§2021-11-14 11:40:48
J.M. WESTON Mocassin 180§150§Paris§36§Très bon état§2071588440§87/f4/b1/87f4b152b3d642da3703fc48b32b3e8d39bc7cec.jpg§2021-11-14 11:33:15
Mocassins JB WESTON marron bergeronnette§250§Lans-en-Vercors§38§Très bon état§1963900850§1b/31/11/1b31115ef453cff370bd5ef368f22f48bdd1352d.jpg§2021-04-14 19:15:07
Vends Chaussures je weston§350§Massongy§40§Très bon état§1913966303§5f/89/c1/5f89c1bc4f5eea225c0a1dae3a7cc55c4e7562a8.jpg§2021-01-19 21:21:29
Chaussures Weston Noir§310§Paris§41§Très bon état§1884335910§ab/73/b7/ab73b7a1e7db62aebf3e6327164838514735ff5d.jpg§2020-11-26 10:37:08
Chaussures homme de marques§1§Villeneuve-lès-Maguelone§42§§1521423666§aa/f9/57/aaf957a122a0f2ff6be105e464d9f6ddefa823e4.jpg§2020-09-13 21:42:14
Mocassins + embauchoirs JM WESTON 180 8D box noir§470§Paris§42§§1575047053§14/33/d1/1433d1b7981cd3d01b19ce1e23200356ecfb0c61.jpg§2020-08-19 11:49:41"""

seen = set()
ads = []
for line in RAW.strip().split('\n'):
    parts = line.split('§')
    if len(parts) != 8:
        continue
    title, price, city, shoe_size_eu, condition, ad_id, img_path, date = parts
    full_url = URL + ad_id
    if full_url in seen:
        continue
    seen.add(full_url)
    ads.append({
        "title": title,
        "price": int(price) if price.isdigit() else 0,
        "url": full_url,
        "image": IMG + img_path,
        "city": city,
        "shoe_size_eu": shoe_size_eu,
        "condition": condition,
        "date": date,
    })

out = "/Users/mjl/Desktop/Claude/Auktion.Se/data/leboncoin.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(ads, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(ads)} unique ads to {out}")
