[
    "seq",
    ["set", "x", 100],
    ["set", "one", ["func", [], ["get", "x"]]],
    ["set", "two", 
        ["func", [], 
            [
                "seq",
                ["set", "x", 42],
                ["call", "one", []]
            ]  
        ]
    ],
    ["set", "main", 
        ["func", [],
            ["call", "two", []]
        ]
    ],
    ["call", "main", []]
]