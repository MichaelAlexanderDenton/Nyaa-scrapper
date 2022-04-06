filters= tuple({'no filter', 'no remake', 'trusted only'})

# m_cat = "Anime"
# s_cat = "Raw"

cats = [
    {"All Categories": [None]},
    {"Anime" : [
        "None",
        "Anime Music Video", 
        "English-translated", 
        "Non-English-translated",
        "Raw",
        ]
     },
    {"Audio": [
        "None",
        "Lossless",
        "Lossy"
    ]
    },
    {"Literature":[
        "None",
        "English-translated", 
        "Non-English-translated",
        "Raw",  
    ]
    },
    {"Raw Action": [
        "None",
        "English-translated",
        "Idol/Promotional Video",
        "Non-English-translated",
        "Raw",  
    ]
    },
    {"Pictures":[
        "None",
        "Graphics",
        "Photos"
    ]
    },
    {"Software": [
        "None",
        "Applications",
        "Games"
    ]}
]

def _create_category_query(category=tuple) -> str():
    user_main_cat = category[0]
    user_sub_cat = category[1]
    print("main cat {0}. sub cat {1}".format(user_main_cat, user_sub_cat))
    main_cat = str()
    sub_cat = str()
    for i, c in enumerate(cats):
        if user_main_cat == "All Categories" or user_main_cat is None:
            main_cat = "0"
            sub_cat = "0"
            break
        for value, key in c.items():
            if value == user_main_cat:
                main_cat = i
                for v, k in enumerate(key):
                    if k == user_sub_cat:
                        sub_cat = v
    print("Main category: {0} - sub-category:{1}".format(main_cat, sub_cat))
    return "{0}_{1}".format(main_cat, sub_cat)
    
def _create_filters_query(_filter):
    if _filter in filters:
        return filters.index(_filter)
    else:
        raise ValueError('Invalid filter input. check documentation for more info.')
        
             
     
                    
_create_category_query(category=("Anime", "English-translated"))

