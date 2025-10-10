[
    "seq",
    ["set", "a_plus_b", 
        ["func", ["a", "b"], 
            ["add", ["get", "a"], ["get", "b"]]
        ]
    ],
    ["set", "a_plus_b_squared", 
        ["func", ["a", "b"], 
            ["power", ["call", "a_plus_b", ["get", "a"], ["get", "b"]], 2]
        ]
    ],
    ["call", "a_plus_b_squared", 3, 2]
]
