from cefpython3 import cefpython as cef
import base64
import platform
import sys
import threading

from simulator import Simulator
from world.position import Position
from world.animal import Animal
from world.plant import Plant
from world.animals.antelope import Antelope
from world.animals.fox import Fox
from world.animals.human import Human
from world.animals.sheep import Sheep
from world.animals.cybersheep import CyberSheep
from world.animals.turtle import Turtle
from world.animals.wolf import Wolf
from world.plants.belladonna import Belladonna
from world.plants.grass import Grass
from world.plants.guarana import Guarana
from world.plants.sowthistle import SowThistle
from world.plants.pineborscht import PineBorscht

class Desiigner:

    HTML_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style type="text/css">
        body,html { font-family: Arial; font-size: 11pt; }
        div.msg { margin: 0.2em; line-height: 1.4em; }
        b { background: #ccc; font-weight: bold; font-size: 10pt;
            padding: 0.1em 0.2em; }
        b.Python { background: #eee; }
        i { font-family: Courier new; font-size: 10pt; border: #eee 1px solid;
            padding: 0.1em 0.2em; }
        h1, h2 { margin-top: 0; }
        h2 { text-align: center; }
            
        table.game tbody tr td { height: 40px; width: 40px; vertical-align: middle; text-align: center; }
        table.game tbody tr td.plant { background-color: rgba(0, 255, 0, 0.5); }
        table.game tbody tr td.human { background-color: rgba(0, 0, 255, 0.5); }
        table.game tbody tr td.animal { background-color: rgba(255, 0, 0, 0.5); }
        #window_bg { display: none; position: fixed; left: 0%; top: 0%; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8);}
        #window{ display: none; position: fixed; left: 30%; top: 30%; width: 20%; height: 20%; background-color: rgba(255,255,255,1); padding: 15px; }
        
        #window input { width:40%; padding: 2.5%; margin: 0%; }
        #window select, #window button { width:95%; padding: 2.5%; margin-top: 5%; }
        
            .hexagon-row {margin-bottom:-10px;}
            .hexagon-row:nth-child(odd) {margin-left:20px;}
            .hexagon-grid {margin-bottom:10px;}
            .hexagon {position:relative;width:40px; height: 23.09px;margin:11.55px 0 11.55px 6px;display:inline-block;}
            .hexagon:before, .hexagon:after {content:"";position: absolute;width:0;border-left:20px solid transparent;border-right:20px solid transparent;}
            .hexagon span {display:block;position:absolute;width:100%;text-align:center;}
            .hexagon:before {bottom:100%;}
            .hexagon:after {top:100%;width:0;}
            
            .hexagon { background-color: rgba(200,200,200,0.5); }
            .hexagon:before { border-bottom: 11.55px solid rgba(200,200,200,0.5); }
            .hexagon:after { border-top: 11.55px solid rgba(200,200,200,0.5); }
            .hexagon.human { background-color: rgba(0,0,255,0.5); }
            .hexagon.human:before { border-bottom: 11.55px solid rgba(0,0,255,0.5); }
            .hexagon.human:after { border-top: 11.55px solid rgba(0,0,255,0.5); }
            .hexagon.animal { background-color: rgba(255,0,0,0.5); }
            .hexagon.animal:before { border-bottom: 11.55px solid rgba(255,0,0,0.5); }
            .hexagon.animal:after { border-top: 11.55px solid rgba(255,0,0,0.5); }
            .hexagon.plant { background-color: rgba(0,255,0,0.5); }
            .hexagon.plant:before { border-bottom: 11.55px solid rgba(0,255,0,0.5); }
            .hexagon.plant:after { border-top: 11.55px solid rgba(0,255,0,0.5); }
        </style>
        <script>
        
        var drawType = 'square';
        var turnAvailable = true;
        var turnTimeout = null;
        
        function js_print(lang, event, msg) {
            msg = "<b class="+lang+">"+lang+": "+event+":</b> " + msg;
            console = document.getElementById("console")
            console.innerHTML += "<div class=msg>"+msg+"</div>";
        }
        function js_callback_1(ret) {
            js_print("Javascript", "html_to_data_uri", ret);
        }
        function js_callback_2(msg, py_callback) {
            js_print("Javascript", "js_callback", msg);
            py_callback("test xD");
        }
        
        function grid_draw(type, x, y) {
            var text = "";
            drawType = type;
            if(type == 'square') {
                text = '<table class="game" border="1"><tbody>';
                for(pos_y = 0; pos_y < y; pos_y++) {
                    text += '<tr id="row_' + pos_y + '">';
                    for(pos_x = 0; pos_x < x; pos_x++) {
                        text += '<td id="col_' + pos_x + '" oncontextmenu="return context(' + pos_x + ', ' + pos_y + ');"></td>';
                    }
                    text += '</tr>';
                }
                text += '</tbody></table>';
            }
            if(type == 'hex') {
                text = '<div class="hexagon-grid">';
                for(pos_y = 0; pos_y < y; pos_y++) {
                    text += '<div id="row_' + pos_y + '" class="hexagon-row">';
                    for(pos_x = 0; pos_x < x; pos_x++) {
                        text += '<div id="col_' + pos_x + '" class="hexagon" oncontextmenu="return context(' + pos_x + ', ' + pos_y + ');"></div>';
                    }
                    text += '</div>';
                }
                text += '</div>';
            }
            document.getElementById("game").innerHTML = text;
        }
        
        function fill_area(x, y, content, cl) {
            var element = document.querySelector("#row_" + y + " #col_" + x);
            if(element) {
                element.className = (drawType == 'hex' ? 'hexagon ' : '') + cl;
                element.innerHTML = drawType == 'hex' ? ('<span>' + content +  '</span>') :  (content);
            }
        }
        
        window.onload = function(){
            js_print("Javascript", "window.onload", "Called");
            js_print("Javascript", "python_property", python_property);
            js_print("Javascript", "navigator.userAgent", navigator.userAgent);
            js_print("Javascript", "cefpython_version", cefpython_version.version);
            html_to_data_uri("test", js_callback_1);
            external.test_multiple_callbacks(js_callback_2);
            external.draw();
        };
        
        document.addEventListener("keydown", keyDownTextField, false);

        function keyDownTextField(e) {
            var keyCode = e.keyCode;
            if(turnAvailable) {
                if(drawType == 'square') {
                    switch(keyCode) {
                        case 37:
                            turn(-1, 0);
                            return false;
                        case 38:
                            turn(0, -1);
                            return false;
                        case 39:
                            turn(1, 0);
                            return false;
                        case 40:
                            turn(0, 1);
                            return false;
                        default:
                            break;
                    }
                }
                else if(drawType == 'hex') {
                    switch(keyCode) {
                        case 70:
                            turn(-1, 0);
                            return false;
                        case 72:
                            turn(1, 0);
                            return false;
                        case 84:
                            turn(0, -1);
                            return false;
                        case 89:
                            turn(1, -1);
                            return false;
                        case 86:
                            turn(0, 1);
                            return false;
                        case 66:
                            turn(1, 1);
                            return false;
                        default:
                            break;
                    }
                }
            }
            switch(keyCode) {
                case 32:
                    external.turn(0, 0);
                    return false;
                case 67:
                    document.getElementById("console").style.display = document.getElementById("console").style.display == "block" ? "none" : "block";
                    return false;
                case 76:
                    load();
                    return false;
                case 83:
                    save();
                    return false;
                case 82:
                    showResize();
                    return false;
                case 27:
                    document.querySelector("#window_bg").style.display = "none";
                    document.querySelector("#window").style.display = "none";
                    return false;
                default:
                    break;
            }
        }
        
        function turn(x, y) {
            external.turn(x, y);
            turnAvailable = false;
            if(turnTimeout) {
                clearTimeout(turnTimeout);
            }
            turnTimeout = setTimeout(function() { turnAvailable = true; }, 500);
        }
        
        function context(x, y) {
            document.querySelector("#window #organism").style.display = "block";
            document.querySelector("#window #grid").style.display = "none";
            document.querySelector("#window_bg").style.display = "block";
            document.querySelector("#window").style.display = "block";
            document.querySelector("#window #organism [name=x]").value = x;
            document.querySelector("#window #organism [name=y]").value = y;
            return false;
        }
        
        function showResize() {
            document.querySelector("#window #organism").style.display = "none";
            document.querySelector("#window #grid").style.display = "block";
            document.querySelector("#window_bg").style.display = "block";
            document.querySelector("#window").style.display = "block";
            document.querySelector("#window #grid [name=x]").value = '';
            document.querySelector("#window #grid [name=y]").value = '';
            return false;
        }
        
        function add() {
            var select = document.querySelector("#window #organism [name=organism]");
            external.add_organism(select.value, document.querySelector("#window #organism [name=x]").value, document.querySelector("#window #organism [name=y]").value);
            document.querySelector("#window_bg").style.display = "none";
            document.querySelector("#window").style.display = "none";
            external.render();            
        }
        
        function load() {
            external.load();
        }
        
        function save() {
            external.save();
        }
        
        function resize() {
            document.querySelector("#window_bg").style.display = "none";
            document.querySelector("#window").style.display = "none";
            external.resize(Math.max(0, parseInt(document.querySelector("#grid [name=x]").value)), Math.max(0, parseInt(document.querySelector("#grid [name=y]").value)), document.querySelector("#grid [name=type]").value);
        }
        </script>
    </head>
    <body>
        <div style="vertical-align:top;">
            <div style="float:left;">
                <h1>Virtual World Simulator</h1>
                <div id="game"></div>
            </div>
            <div style="float:right;text-align:left;">
                <h2>Help</h2>
                L - Load world<br/>
                S - Save world<br/>
                R - Change grid<br/>
                SPACE - Special ability (Alzur`s Shield)<br/>
                ESC - Close pop-up<br/>
                RIGTH CLICK - add organism <br/><br/><br/>
                <b>Square grid movement:</b><br/><br/>
                <table class="game" border="1"><tbody>
                    <tr>
                        <td></td><td>UP</td><td></td>
                    </tr>
                    <tr>
                        <td>LEFT</td><td class="human"></td><td>RIGHT</td>
                    </tr>
                    <tr>
                        <td></td><td>DOWN</td><td></td>
                    </tr>
                </tbody></table><br/><br/>
                <b>Hexagonal grid movement:</b><br/><br/>
                <div class="hexagon-grid">
                    <div class="hexagon-row">
                        <div class="hexagon"><span>T</span></div>
                        <div class="hexagon"><span>Y</span></div>
                    </div>
                    <div class="hexagon-row">
                        <div class="hexagon"><span>F</span></div>
                        <div class="hexagon human"></div>
                        <div class="hexagon"><span>H</span></div>
                    </div>
                    <div class="hexagon-row">
                        <div class="hexagon"><span>V</span></div>
                        <div class="hexagon"><span>B</span></div>
                    </div>
                </div>
            </div>
            <div style="clear:both;"></div>
        </div>
        <div style="clear:both;"></div>
        <div id="console" style="display:none;"></div>
        <div id="window_bg"></div>
        <div id="window">
            <div id="organism">
                <h2>Add organism</h2>
                <input type="number" name="x" placeholder="x" />
                <input type="number" name="y" placeholder="y" />
                <select name="organism">
                    <optgroup label="Animals">
                        <option value="Antelope">Antelope</option>
                        <option value="CyberSheep">Cyber Sheep</option>
                        <option value="Fox">Fox</option>
                        <option value="Human">Human</option>
                        <option value="Sheep">Sheep</option>
                        <option value="Turtle">Turtle</option>
                        <option value="Wolf">Wolf</option>
                    </optgroup>
                    <optgroup label="Plants">
                        <option value="Belladonna">Belladonna</option>
                        <option value="Grass">Grass</option>
                        <option value="Guarana">Guarana</option>
                        <option value="SowThistle">Sow Thistle</option>
                        <option value="PineBorscht">Pine Borscht</option>
                    </optgroup>
                </select>
                <button onclick="add();">Create</button>
            </div>
            <div id="grid">
                <h2>Change grid</h2>
                <input type="number" name="x" placeholder="x" />
                <input type="number" name="y" placeholder="y" />
                <select name="type">
                    <option value="square">Square grid</option>
                    <option value="hex">Hexagonal grid</option>
                </select>
                <button onclick="resize();">Change</button>
            </div>
        </div>
    </body>
    </html>
    """

    def __init__(self, simulator):
        self.check_versions()
        self.simulator = simulator
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        # To change user agent use either "product_version"
        # or "user_agent" options. Explained in Tutorial in
        # "Change user agent string" section.
        settings = {
            # "product_version": "MyProduct/10.00",
            # "user_agent": "MyAgent/20.00 MyProduct/10.00",
        }
        cef.Initialize(settings=settings)
        self.set_global_handler()
        self.browser = cef.CreateBrowserSync(url=self.html_to_data_uri(self.HTML_code), window_title="Dawid Martenczuk 165408")
        """self.set_client_handlers()"""
        self.set_javascript_bindings()

    def exit(self):
        cef.MessageLoop()
        cef.Shutdown()

    def check_versions(self):
        ver = cef.GetVersion()
        print("[tutorial.py] CEF Python {ver}".format(ver=ver["version"]))
        print("[tutorial.py] Chromium {ver}".format(ver=ver["chrome_version"]))
        print("[tutorial.py] CEF {ver}".format(ver=ver["cef_version"]))
        print("[tutorial.py] Python {ver} {arch}".format(
               ver=platform.python_version(),
               arch=platform.architecture()[0]))
        assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"

    def html_to_data_uri(self, html, js_callback=None):
        # This function is called in two ways:
        # 1. From Python: in this case value is returned
        # 2. From Javascript: in this case value cannot be returned because
        #    inter-process messaging is asynchronous, so must return value
        #    by calling js_callback.
        html = html.encode("utf-8", "replace")
        b64 = base64.b64encode(html).decode("utf-8", "replace")
        ret = "data:text/html;base64,{data}".format(data=b64)
        if js_callback:
            self.js_print("Python", "html_to_data_uri", "Called from Javascript. Will call Javascript callback now.")
            js_callback.Call(ret)
        else:
            return ret

    def set_global_handler(self):
        # A global handler is a special handler for callbacks that
        # must be set before Browser is created using
        # SetGlobalClientCallback() method.
        """global_handler = GlobalHandler()
        cef.SetGlobalClientCallback("OnAfterCreated",
                                    global_handler.OnAfterCreated)"""

    """def set_client_handlers(self):
        client_handlers = [LoadHandler(), DisplayHandler()]
        for handler in client_handlers:
            self.browser.SetClientHandler(handler)"""

    def set_javascript_bindings(self):
        external = External(self)
        bindings = cef.JavascriptBindings(
                bindToFrames=False, bindToPopups=False)
        bindings.SetProperty("python_property", "This property was set in Python")
        bindings.SetProperty("cefpython_version", cef.GetVersion())
        bindings.SetFunction("html_to_data_uri", self.html_to_data_uri)
        bindings.SetObject("external", external)
        self.browser.SetJavascriptBindings(bindings)

    def js_print(self, lang, event, msg):
        # Execute Javascript function "js_print"
        self.browser.ExecuteFunction("js_print", lang, event, msg)


class External(object):
    def __init__(self, desiigner):
        self.desiigner = desiigner
        self.draw()

    def save(self):
        self.desiigner.simulator.save()

    def load(self):
        self.desiigner.simulator.load()
        self.draw()
        self.render()

    def resize(self, x, y, type):
        del self.desiigner.simulator
        self.desiigner.simulator = Simulator(x, y, type)
        self.draw()
        self.render()

    def draw(self):
        self.desiigner.browser.ExecuteFunction("grid_draw", self.desiigner.simulator.type, self.desiigner.simulator.size.x, self.desiigner.simulator.size.y)

    def render(self):
        for x in range(self.desiigner.simulator.size.x):
            for y in range(self.desiigner.simulator.size.y):
                organism = self.desiigner.simulator.find_organism(Position(x, y))
                if organism is None:
                    self.desiigner.browser.ExecuteFunction("fill_area", x, y, "", "")
                else:
                    if isinstance(organism, Plant):
                        self.desiigner.browser.ExecuteFunction("fill_area", x, y, organism.shortcut, "plant")
                    elif isinstance(organism, Human):
                        self.desiigner.browser.ExecuteFunction("fill_area", x, y, organism.shortcut, "human")
                    elif isinstance(organism, Animal):
                        self.desiigner.browser.ExecuteFunction("fill_area", x, y, organism.shortcut, "animal")

    def turn(self, x, y):
        self.desiigner.simulator.execute_turn(Position(int(x), int(y)))
        self.render()

    def add_organism(self, name, x, y):
        print(name + ", " + str(x) + ", " + str(y))
        position = Position(int(x), int(y))
        self.desiigner.simulator.add_organism(position, eval(name)(self.desiigner.simulator, position))

    def test_multiple_callbacks(self, js_callback):
        """Test both javascript and python callbacks."""
        self.desiigner.js_print("Python", "test_multiple_callbacks", "Called from Javascript. Will call Javascript callback now.")

        def py_callback(msg_from_js):
            self.desiigner.js_print("Python", "py_callback", msg_from_js)
            print(msg_from_js)
        js_callback.Call("test", py_callback)


def main():
    desiigner = Desiigner(Simulator(15, 15, "square"))
    desiigner.exit()

if __name__ == '__main__':
    main()