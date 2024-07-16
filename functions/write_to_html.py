import json, traceback

# scan_results = [{"contentLength": "199B ", "contentType": "text/html", "redirect": "", "status": 403, "statusColorClass": "text-danger", "url": "http://cpag.ioc.u-tokyo.ac.jp/config.php~"}, {"contentLength": "199B ", "contentType": "text/html", "redirect": "", "status": 403, "statusColorClass": "text-danger", "url": "http://jeast.ioc.u-tokyo.ac.jp/config.php~"}]

row_html_content = """
<!DOCTYPE html>
<html>
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.js" integrity="sha384-ma9ivURrHX5VOB4tNq+UiGNkJoANH4EAJmhxd1mmDq0gKOv88wkKZOfRDOpXynwh" crossorigin="anonymous"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0" crossorigin="anonymous">
<script>
function openURLs(){
  var table = document.getElementsByClassName("table")[0];
  for (let row of table.rows) {
      let val = row.cells[0].innerText;
      if (val == "URL" || val == null)
        continue;
      window.open(val, '_blank');
  }
}
function search(app, result) {
    return app.searchQuery.toLowerCase().split(" ").every(
      (v) => result.url.toLowerCase().includes(v) ||
      (result.contentType && result.contentType.toLowerCase().includes(v)) ||
      result.contentLength.toLowerCase().includes(v) ||
      result.status.toString().includes(v) ||
      (result.redirect && result.redirect.toLowerCase().includes(v))
    );
}
function statusExcludeSearch(app, result){
    return app.statusExcludeSearchQuery.toLowerCase().split(" ").every(
      (v) => !result.status.toString().includes(v)
    );
}
function lengthExcludeSearch(app, result){
    return app.lengthExcludeSearchQuery.toLowerCase().split(" ").every(
      (v) => !result.contentLength.toLowerCase().includes(v)
    );
}
window.onload = function () {
    var app = new Vue({
      el: '#app',
      delimiters: ['[[', ']]'],
      data() {
        return {
            lengthExcludeSearchQuery: null,
            statusExcludeSearchQuery: null,
            searchQuery: null,
            resources: []
        };
      },
      methods: {
        urlJoin: function(url, redirect){
          return new URL(redirect, url).href;
        }
      },
      computed: {
        resultQuery(){
          var arr = null;
          if(this.searchQuery){
            arr = this.resources.filter((result)=>{
              return search(this, result)
            });
            
            if(!this.statusExcludeSearchQuery && !this.lengthExcludeSearchQuery)
              return arr;
          }
          if(this.statusExcludeSearchQuery){
            var arrStatusExcluded = null;
            if(arr){
              arrStatusExcluded = arr.filter((result)=>{
                return statusExcludeSearch(this, result)
              });
              if(!this.lengthExcludeSearchQuery)
                return arrStatusExcluded;
            }
            else{
              arrStatusExcluded = this.resources.filter((result)=>{
                return statusExcludeSearch(this, result)
              });
              if(!this.lengthExcludeSearchQuery)
                return arrStatusExcluded; 
            }
          }
          if(this.lengthExcludeSearchQuery){
            if(arrStatusExcluded){
              return arrStatusExcluded.filter((result)=>{
                return lengthExcludeSearch(this, result)
              })
            }
            else if(arr){
              return arr.filter((result)=>{
                return lengthExcludeSearch(this, result)
              })
            }
            else{
              return this.resources.filter((result)=>{
                return lengthExcludeSearch(this, result)
              })  
            }
          }
          else{
            return this.resources;
          }
        }
      }
    });
}
</script>
</head>
<body style="background-color: #3f3f3f;">
    <div id="app">
        <div class="panel panel-default">
            <div class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="p-3">
                    <h1><a href="https://xx.com" style="text-decoration:none;color:#c84949;">dirfuzz</a></h1>
                </div>
            </div>
            <br>
            <div class="w-75 p-3 mx-auto">
                
                <br>
                <div class="row">
                    <div class="search-wrapper panel-heading col-sm-4">
                        <input class="form-control" type="text" v-model="statusExcludeSearchQuery" placeholder="Exclude status codes, separated by space" />
                    </div>
                    <div class="search-wrapper panel-heading col-sm-4">
                        <input class="form-control" type="text" v-model="lengthExcludeSearchQuery" placeholder="Exclude content lengths, separated by space" />
                    </div>
                    <div class="col-sm-4">
                      <button onclick="openURLs()" type="button" class="btn btn-danger">Open URLs</button>
                    </div>
                    <br>
                    <br>
                    <div class="search-wrapper panel-heading col-sm-12">
                        <input class="form-control" type="text" v-model="searchQuery" placeholder="Search" />
                    </div>
                </div>
                <br>
                <div class="table-responsive">
                    <table v-if="resources.length" class="table">
                        <tbody>
                            <tr style="color: aliceblue;">
                                <th>URL</th>
                                <th>Status</th>
                                <th>Content Length</th>
                                <th>Content Type</th>
                                <th>Redirect</th>
                            </tr>
                            <tr v-for="result in resultQuery">
                                <td><a class="text-decoration-none" v-bind:class="result.statusColorClass" v-bind:href="result.url" target="_blank">[[result.url]]</a></td>
                                <td><a class="text-decoration-none" v-bind:class="result.statusColorClass" target="_blank">[[result.status]]</a></td>
                                <td style="color: aliceblue;"><a target="_blank">[[result.contentLength]]</a></td>
                                <td style="color: aliceblue;"><a target="_blank">[[result.contentType]]</a></td>
                                <td><a class="text-decoration-none" v-bind:href="urlJoin(result.url, result.redirect)" target="_blank">[[result.redirect]]</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>

"""

n = 1
def write_results_to_html(scan_results, outputFile):
    try:
        global n
        # print(outputFile)
        # 读取 HTML 文件内容

        if n == 1:
            html_content = row_html_content
        else:
            with open(outputFile, 'r', encoding="utf-8") as f:    
                html_content = f.read()
    

        # 找到 Vue.js 应用中的 resources 数据位置
        resources_start_index = html_content.find('resources: [') + len('resources: [')
        resources_end_index = html_content.find(']', resources_start_index)

        # 获取原始的 resources 列表内容
        resources_str = html_content[resources_start_index:resources_end_index].strip()

        # 如果原始的 resources 列表内容不为空，则在其末尾添加逗号，以便追加新数据
        if resources_str and not resources_str.endswith(','):
            resources_str += ','

        # 将扫描结果转换为 JavaScript 对象数组的字符串表示形式
        scan_results_js = ',\n'.join([json.dumps(result) for result in scan_results])

        # 将新的扫描结果追加到现有的 resources 列表中
        updated_resources_str = resources_str + scan_results_js

        # 将更新后的 resources 列表替换回 HTML 文件中
        updated_html_content = (
            html_content[:resources_start_index] +
            updated_resources_str +
            html_content[resources_end_index:]
        )

        # 写回更新后的 HTML 文件内容
        with open(outputFile, 'w', encoding="utf-8") as f:
            f.write(updated_html_content)
        # print("保存完毕！")
        n += 1

    except:  
        # traceback.print_exc()
        pass
