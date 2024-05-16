import os
from colorama import Fore, Style

def generate_html_report(project_folder, project_name, screenshots):
    report_file = os.path.join(project_folder, "report.html")
    with open(report_file, "w") as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
        }}
        h1, h2 {{
            color: #e0e0e0;
        }}
        .container {{
            padding: 20px;
        }}
        .screenshot {{
            margin: 10px;
        }}
        .screenshot img {{
            border: 1px solid #333;
            border-radius: 4px;
            padding: 5px;
            width: 300px;
        }}
        .screenshot img:hover {{
            box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
        }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1;
            padding-top: 100px;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgb(0,0,0);
            background-color: rgba(0,0,0,0.9);
        }}
        .modal-content {{
            margin: auto;
            display: block;
            width: 80%;
            max-width: 700px;
        }}
        .modal-content {{
            -webkit-animation-name: zoom;
            -webkit-animation-duration: 0.6s;
            animation-name: zoom;
            animation-duration: 0.6s;
        }}
        @-webkit-keyframes zoom {{
            from {{ -webkit-transform: scale(0) }}
            to {{ -webkit-transform: scale(1) }}
        }}
        @keyframes zoom {{
            from {{ transform: scale(0) }}
            to {{ transform: scale(1) }}
        }}
        .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
        }}
        .close:hover,
        .close:focus {{
            color: #bbb;
            text-decoration: none;
            cursor: pointer;
        }}
        @media only screen and (max-width: 700px) {{
            .modal-content {{
                width: 100%;
            }}
        }}
        .toggle-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #333;
            color: #fff;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 4px;
        }}
        .light-mode {{
            background-color: #ffffff;
            color: #000000;
        }}
        .light-mode h1, .light-mode h2 {{
            color: #000000;
        }}
        .light-mode img {{
            border: 1px solid #ddd;
        }}
        .gallery {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }}
        .server-headers {{
            font-size: 14px;
            margin-top: 5px;
            color: #888;
        }}
    </style>
</head>
<body>
    <button class="toggle-button" onclick="toggleMode()">Dark/Light Mode</button>
    <div class="container">
        <center><h1>{project_name}</h1></center>
        <div class="gallery">
""")
        for screenshot in screenshots:
            relative_path = os.path.relpath(screenshot['filename'], start=project_folder)
            f.write(f"""
            <div class="screenshot">
                <h2>{screenshot['url']}</h2>
                <img src="{relative_path}" alt="{screenshot['url']}" onclick="openModal(this.src)">
                <div class="server-headers">
                    Server Header Value: {screenshot.get('server_header', 'N/A')}
                </div>
            </div>
""")
        f.write("""
        </div>
    </div>
    <div id="myModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="img01">
    </div>
    <script>
        function openModal(src) {
            var modal = document.getElementById("myModal");
            var modalImg = document.getElementById("img01");
            modal.style.display = "block";
            modalImg.src = src;
        }
        function closeModal() {
            var modal = document.getElementById("myModal");
            modal.style.display = "none";
        }
        function toggleMode() {
            document.body.classList.toggle('light-mode');
        }
    </script>
</body>
</html>
""")
    print(Fore.YELLOW + "=" * 50)
    print(Fore.YELLOW + f"HTML report generated: {report_file}")
    print(Fore.YELLOW + "=" * 50)
