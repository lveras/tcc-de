<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Sistema de aferição de temperatura multi sensores.</title>

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
        integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

        <!-- Optional theme -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"
        integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
        <style>
            .resp-iframe {
                position: absolute;
                top: 0;
                left: 0;
                margin-top: 30px;
                width: 100%;
                height: 90%;
                border: 0;
            }
        </style>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script>
            window.setInterval("reloadIFrame();", 30000);

            function reloadIFrame() {
                $('#table_plot').attr('src', $('#table_plot').attr('src'));
            }

        </script>
    </head>

    <body>
        <div class="container">
            <div class="row">
                <div class="col-xs-12">
                    <div class="page">
	                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#modalConfig">
                          Configurações
                        </button>

                        <div class="resp-container">
                            <iframe name="table_plot" id="table_plot" class="resp-iframe" src="table_plot" allowfullscreen></iframe>
                        </div>
                     </div>
                </div>
            </div>
    </body>
    <footer>
        <div class="modal fade" id="modalConfig" tabindex="-1" role="dialog">
          <div class="modal-dialog modal-lg" style='height:80%;' role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h3 class="modal-title">Configurações</h3>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <div class="embed-responsive embed-responsive-4by3">
                    <iframe class="embed-responsive-item" src="config" ></iframe>
                </div>
              </div>
            </div>
          </div>
        </div>

      </footer>
</html>