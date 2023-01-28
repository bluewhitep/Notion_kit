####################################################################################
# MIT License
#
# Copyright (c) 2023 bluewhitep
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################################

TEXT_COLOR_LIST=[
                 "blue",    "blue_background",
                 "brown",   "brown_background",
                 "default",
                 "gray",    "gray_background",
                 "green",   "green_background",
                 "orange",  "orange_background",
                 "pink",    "pink_background",
                 "purple",  "purple_background",
                 "red",     "red_background",
                 "yellow",  "yellow_background"
]
     
#---------------------[Property]---------------------#            
ALL_PROPERTIES_TYPES = [
                        "title", "rich_text", "number",  "select", "multi_select",
                        "status", "date", "people", "files", "checkbox", "url", 
                        "email", "phone_number",  "relation", "formula", "rollup",
                        "created_time",  "created_by", 
                        "last_edited_time", "last_edited_by",
]

NON_CREATEABLE_PROPERTIES_TYPES = [
                                    "title",  # Because it is created by default
                                    "status", # Not Recommended [Non-update property type]. Because it is can not add Groups and Options 
                                    "rollup", # Because it is need know "relation_property_id" and "rollup_property_id"
]

NON_UPDATABLE_PROPERTIES_TYPES = [
                                    "status",  # Because it is not a valid property schema by Notion API
]

NON_UPDATABLE_PROPERTIES_ITEMS = [
                                  "created_time", "created_by",
                                  "last_edited_time", "last_edited_by",
                                  "formula", "rollup",
]

FORMAT_TYPES = [
                "number", "number_with_commas", "percent", "dollar",
                "canadian_dollar", "euro", "pound", "yen", "ruble", "rupee", 
                "won", "yuan", "real", "lira", "rupiah", "franc", 
                "hong_kong_dollar", "new_zealand_dollar", "krona", 
                "norwegian_krone", "mexican_peso", "rand", "new_taiwan_dollar", 
                "danish_krone", "zloty", "baht", "forint", "koruna", "shekel", 
                "chilean_peso", "philippine_peso", "dirham", "colombian_peso", 
                "riyal", "ringgit", "leu", "argentine_peso", "uruguayan_peso", 
                "singapore_dollar",
]

ROLLUP_FUNCTION_LIST = [
                        "count_all", "count_values", "count_unique_values", 
                        "count_empty", "count_not_empty", 
                        "percent_empty", "percent_not_empty", 
                        "sum", "average", "median", "min", "max", "range", 
                        "show_original",
]

ROLLUP_TYPE_LIST = [
                    "number", "date", "array", "unsupported", "incomplete"
]

#---------------------[Block]---------------------#

BLOCK_CHILDREN_TYPES = [
                        "block", 
                        "page", 
                        "user", 
                        "database", 
                        "property_item", 
                        "page_or_database"
]

BLOCK_TYPE_LIST = [
                    "paragraph", "heading_1", "heading_2", "heading_3", 
                    "callout", "quote", "bulleted_list_item",
                    "numbered_list_item", "to_do", "toggle", "code",
                    "child_page", "child_database",
                    "embed", "bookmark", "link_preview", 
                    "image", "video", "pdf", "equation",
                    "divider",
                    "table_of_contents", "breadcrumb",
                    "template", "link_to_page", "synced_block",
                    "column_list", "column", "table", "table_row",
]

CODE_LANGUAGE_LIST =[
                    "abap", "arduino", "bash", "basic", "c", "clojure", 
                    "coffeescript",  "c++", "c#", "css", "dart", "diff",
                    "docker", "elixir", "elm", "erlang", "flow", "fortran",
                    "f#", "gherkin", "glsl", "go", "graphql", "groovy",
                    "haskell", "html", "java", "javascript", "json",
                    "julia", "kotlin", "latex", "less", "lisp", "livescript",
                    "lua", "makefile", "markdown", "markup", "matlab",
                    "mermaid", "nix", "objective-c", "ocaml", "pascal",
                    "perl", "php", "plain text", "powershell", "prolog",
                    "protobuf", "python", "r", "reason", "ruby", "rust",
                    "sass", "scala", "scheme", "scss", "shell", "sql",
                    "swift", "typescript", "vb.net", "verilog", "vhdl",
                    "visual basic", "webassembly", "xml", "yaml",
                    "java/c/c++/c#",
]

MEDIA_TYPE_LIST = [
                    "image", "video", "file", "pdf",
]