<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Sistema de aferição de temperatura multi sensores.</title>

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
        integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

        <!-- Optional theme -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"
        integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

        <script>
            $('document').ready(function(){
                $('div.alert').delay(5000).fadeOut('slow');
            })
        </script>
    </head>

    <body>
        <div class="container">
            <div class="row">
                <div class="page">
                    <form action="/save-config" method="post">
                        %if s:
                        <div class="alert alert-success" role="alert">
                          Configurações salvas com sucesso!
                        </div>
                        %end
                        <h4>Temperatura mínima e máxima geral para alerta</h4>
                        <p class='col-sm-12 small-text text-danger'>*Se não definido minimo e máximo para o sensor, este será o valor para alerta.</p>

                        <div class="form-group row">
                            <label for="min_geral" class="col-sm-2 col-form-label">Minimo</label>
                            <div class="col-sm-4">
                                <input type="number" value="{{min_geral or 20}}" class="form-control" id="min_geral" name="min_geral"/>
                            </div>
                            <label for="max_geral" class="col-sm-2 col-form-label">Máximo</label>
                            <div class="col-sm-4">
                                <input type="number" value="{{max_geral or 25}}" class="form-control" id="max_geral" name="max_geral"/>
                            </div>
                        </div>

                        <h4>SMTP</h4>
                        <div class="form-group row">
                            <label for="smtp_server" class="col-sm-2 col-form-label">Servidor SMTP</label>
                            <div class="col-sm-7">
                                <input type="text" class="form-control" id="smtp_server" name="smtp_server" value="{{smtp_server or ''}}" />
                            </div>
                            <label for="smtp_server" class="col-sm-1 col-form-label">Porta</label>
                            <div class="col-sm-2">
                                <input type="text" class="form-control" id="smtp_port" name="smtp_port" value="{{smtp_port or ''}}" />
                            </div>
                        </div>

                        <div class="form-group row">
                            <label for="smtp_email" class="col-sm-2 col-form-label">Login</label>
                            <div class="col-sm-4">
                                <input type="text" class="form-control" id="smtp_email" name="smtp_email" value="{{smtp_email or ''}}" />
                            </div>
                            <label for="smtp_password" class="col-sm-2 col-form-label">Senha</label>
                            <div class="col-sm-4">
                                <input type="password" class="form-control" id="smtp_password" name="smtp_password" value="{{smtp_password or ''}}" />
                            </div>
                        </div>

                        <h4>Emails para alerta</h4>
                        <div class="form-group row">
                            <label for="send_emails" class="col-sm-2 col-form-label">Enviar para</label>
                            <div class="col-sm-10">
                                <input type="send_emails" class="form-control" id="send_emails" name="send_emails" value="{{send_emails or ''}}" placeholder='Separar emails por virgula' />
                            </div>
                        </div>

                        <h4>Sensores</h4>

                        %for s in list_sensores:
                            <div class="form-group row">
                                <label for="{{s[0] or ''}}" class="col-sm-2 col-form-label">Sensor {{s[0] or ''}}</label>
                                <div class="col-sm-4">
                                    <input type="text" class="form-control" id="label_{{s[0] or ''}}" name="label_{{s[0] or ''}}"
                                            placeholder="Ex. Sala de reunião 1"
                                            value="{{s[1] or ''}}"/>
                                </div>
                                <label for="min_{{s[0] or ''}}" class="col-sm-1 col-form-label">Min</label>
                                <div class="col-sm-2">
                                    <input type="number" class="form-control" id="min_{{s[0] or ''}}" name="min_{{s[0] or ''}}"
                                            placeholder="Ex. 19"
                                            value="{{s[2] or ''}}"/>
                                </div>
                                <label for="max_{{s[0] or ''}}" class="col-sm-1 col-form-label">Max</label>
                                <div class="col-sm-2">
                                    <input type="number" class="form-control" id="max_{{s[0] or ''}}" name="max_{{s[0] or ''}}"
                                            placeholder="Ex. 25"
                                            value="{{s[3] or ''}}"/>
                                </div>
                            </div>
                        %end
                    </form>
                </div>
            </div>
        </div>
    </body>
</html>