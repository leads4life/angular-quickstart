import html
S=[("appetizers","Appetizers","點心","Folded, rolled and fried to order.",[
 ("Pork Soup Dumplings","$10.95","Six xiao long bao with pork and a rich ginger broth sealed inside. Sip the soup first.","fav"),
 ("Pan-Fried Pork Potstickers","$9.50","Six dumplings with crisp golden bottoms, black vinegar and ginger dip.",""),
 ("Crab Rangoon","$8.95","Six crisp wontons filled with crab and cream cheese, sweet chili sauce.",""),
 ("Egg Rolls (2)","$4.50","Cabbage, roast pork and carrot in a blistered wrapper.",""),
 ("Vegetable Spring Rolls (2)","$4.50","Shiitake, cabbage and glass noodles, rolled thin and fried crisp.","veg"),
 ("Scallion Pancake","$7.95","Flaky, pan-fried layers with ginger soy dipping sauce.","veg"),
]),("soups","Soups","湯","Pint / quart.",[
 ("Wonton Soup","$4.50 / $8.95","Pork wontons, bok choy and scallion in clear chicken broth.",""),
 ("Hot & Sour Soup","$4.50 / $8.95","Tofu, wood-ear mushroom, bamboo shoots, white pepper and black vinegar.","spicy fav"),
 ("Egg Drop Soup","$3.95 / $7.50","Silky egg ribbons in a light chicken broth.",""),
 ("West Lake Beef Soup","$10.95","Minced beef, egg white and cilantro, quart only.",""),
]),("chicken","Chicken","雞","Served with steamed white rice. Brown rice or fried rice on request.",[
 ("General Tso’s Chicken","$16.95","Crisp chicken in a sweet, tangy and gently spicy glaze with broccoli and sesame.","fav spicy"),
 ("Kung Pao Chicken","$15.95","Wok-tossed with peanuts, dried chilies, Sichuan peppercorn and scallion.","spicy"),
 ("Sesame Chicken","$16.50","Crisp chicken in a honey-soy glaze with toasted sesame.",""),
 ("Orange Chicken","$16.50","Crisp chicken tossed in orange peel sauce.",""),
 ("Moo Goo Gai Pan","$15.50","Sliced chicken with mushrooms, snow peas and water chestnuts in white sauce.",""),
 ("Chicken with Broccoli","$15.50","Tender sliced chicken and broccoli in brown garlic sauce.",""),
]),("beef-pork","Beef &amp; Pork","牛豬","",[
 ("Mongolian Beef","$18.50","Seared flank steak with scallions and onions in a dark, savory glaze.","fav"),
 ("Beef with Broccoli","$17.50","Velveted beef and broccoli in oyster sauce.",""),
 ("Szechuan Beef","$18.50","Shredded crispy beef with carrot, celery and chili.","spicy"),
 ("Pepper Steak","$17.50","Beef with green peppers and onions in black bean sauce.",""),
 ("Twice-Cooked Pork","$16.50","Simmered then wok-fried pork belly with cabbage and chili bean paste.","spicy"),
 ("Sweet &amp; Sour Pork","$15.95","Crisp pork with pineapple, peppers and onion.",""),
]),("seafood","Seafood","海鮮","",[
 ("Honey Walnut Shrimp","$20.50","Crisp jumbo shrimp in a light honey cream with candied walnuts.","fav"),
 ("Salt &amp; Pepper Shrimp","$19.95","Shell-on shrimp fried crisp with garlic, jalapeño and five-spice salt.","spicy"),
 ("Kung Pao Shrimp","$19.50","Shrimp with peanuts, dried chilies and scallion.","spicy"),
 ("Shrimp with Lobster Sauce","$18.95","Shrimp in a silky egg and fermented black bean sauce.",""),
 ("Steamed Whole Fish","Market","Ginger, scallion and hot oil poured tableside, finished with light soy.",""),
]),("noodles","Noodles &amp; Rice","麵飯","",[
 ("Lo Mein","$13.95–$15.95","Soft egg noodles tossed with cabbage, carrot and bean sprouts. Choose vegetable, chicken, pork, beef or shrimp.","fav"),
 ("Beef Chow Fun","$16.50","Wide rice noodles seared with beef, bean sprouts and scallion for real wok hei.",""),
 ("Dan Dan Noodles","$13.50","Wheat noodles, spiced pork, chili oil, sesame paste and Sichuan peppercorn.","spicy"),
 ("Singapore Rice Noodles","$15.50","Thin rice noodles with shrimp, roast pork, egg and curry.","spicy"),
 ("Vegetable Fried Rice","$11.95","Egg, peas, carrot, scallion and bean sprouts.","veg fav"),
 ("Yangzhou Fried Rice","$14.95","Shrimp, roast pork, egg and scallion.",""),
]),("vegetarian","Vegetables &amp; Tofu","素","Made without meat. Tell us about allergies when you order.",[
 ("Ma Po Tofu","$14.50","Our vegetable version: silken tofu and shiitake in chili bean sauce with Sichuan peppercorn.","veg spicy"),
 ("Dry-Fried Green Beans","$13.50","Blistered beans with garlic, chili and preserved mustard greens.","veg"),
 ("Eggplant in Garlic Sauce","$13.95","Chinese eggplant braised in garlic, ginger and chili.","veg spicy"),
 ("Buddha’s Delight","$13.95","Tofu, mushrooms, snow peas, baby corn and napa cabbage in light sauce.","veg"),
 ("Garlic Bok Choy","$11.95","Baby bok choy wok-tossed with garlic.","veg"),
]),("sweets","Sweets","甜","",[
 ("Sesame Balls","$6.50","Four crisp glutinous rice balls filled with red bean paste.","veg"),
 ("Mango Pudding","$5.95","Chilled and creamy, with fresh mango.","veg"),
])]
pep='<svg class="ico" aria-hidden="true"><use href="#i-pepper"/></svg>'
out=[]
cjk=set()
for key,title,zh,note,items in S:
    cjk|=set(zh)
    out.append(f'      <section class="menu-block" id="{key}" aria-labelledby="{key}-h">')
    out.append(f'        <h2 id="{key}-h">{title} <span class="zh" lang="zh" aria-hidden="true">{zh}</span></h2>')
    if note: out.append(f'        <p class="note">{note}</p>')
    out.append('        <ul class="menu">')
    for n,p,d,t in items:
        tags=[]
        if 'fav' in t: tags.append('<span class="tag">House favorite</span>')
        if 'spicy' in t: tags.append(f'<span class="tag spicy">{pep}Spicy</span>')
        if 'veg' in t: tags.append('<span class="tag veg">Vegetarian</span>')
        dt=(t+' all').strip()
        out.append(f'          <li data-tags="{dt}"><div class="mi-top"><span class="mi-name">{n}</span><span class="mi-price">{p}</span></div><p class="mi-desc">{d}</p>{"".join(tags)}</li>')
    out.append('        </ul>\n      </section>')
jump=" ".join(f'<a href="#{k}">{t}</a>' for k,t,*_ in S)
open('work/menu_blocks.html','w').write("\n".join(out))
open('work/menu_jump.html','w').write(jump)
print(''.join(sorted(cjk)))
