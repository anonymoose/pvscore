
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${request.ctx.enterprise.name} CRM</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">


    ${h.stylesheet_link('/static/bootstrap/css/bootstrap.css')}
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
    </style>
    ${h.stylesheet_link('/static/bootstrap/css/bootstrap-responsive.css')}

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="../assets/ico/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="../assets/ico/apple-touch-icon-144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="../assets/ico/apple-touch-icon-114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="../assets/ico/apple-touch-icon-72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="../assets/ico/apple-touch-icon-57-precomposed.png">
  </head>

  <body>

    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <h1>${request.ctx.enterprise.name} CRM Login</h1>
        <p>
          <form method="POST" action="/crm/login">
            <input type="hidden" name="path" value="${request.GET.get('path', '')}"/>
            <input type="hidden" name="vars" value="${request.GET.get('vars', '')}"/>
            <div>
              <label for="username">Username</label>
              ${h.text('username', size=50)}
            </div>
            <div>
              <label for="password">Password</label>
              ${h.password('password', size=50)}
            </div>
            <div>
              <input type="submit" class="btn btn-primary btn-large" value="Login"/>
            </div>
            <div>
              % for flash in request.session.pop_flash():
              <div class="flash" style="font-size:13px">
                ${flash}
              </div>
              % endfor
            </div>
          </form>
        </p>
      </div>

      <hr>

      <footer>
        <p>&copy; ${request.ctx.enterprise.copyright if request.ctx.enterprise.copyright else 'Palm Valley Software'} 2012</p>
      </footer>

    </div> <!-- /container -->

    <script src="/static/bootstrap/js/jquery.js"></script>
    <script src="/static/bootstrap/js/bootstrap.js"></script>

  </body>
</html>
