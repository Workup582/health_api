function init(apiBaseUrl) {
  const COOKIE_NAME = "fam_auth_2_0_0";

  const router = new Navigo(null, true, "#!");

  const templatesCache = {};

  const getToken = () => Cookies.get(COOKIE_NAME);

  const getTemplate = (templateId) => {
    if (!templatesCache[templateId]) {
      const templateElement = document.getElementById(`template-${templateId}`);

      if (templateElement) {
        templatesCache[templateId] = Handlebars.compile(templateElement.innerHTML);
      }
    }

    return templatesCache[templateId];
  };

  const renderTemplate = (templateId, context) => {
    const renderedKey = templateId + JSON.stringify(context);

    if (!templatesCache[renderedKey]) {
      const template = getTemplate(templateId);

      if (template) {
        templatesCache[renderedKey] = template(context).trim();
      }
    }

    return templatesCache[renderedKey] || "";
  };

  const renderPage = (name, context = {}, parentElement = "app") => {
    const parent = document.getElementById(parentElement);
    const content = renderTemplate(name, context);

    console.log(`Rendering page ${name}`);

    parent.innerHTML = content;
  };

  const controls = {
    navBtnLogout: ".header-link-logout",
    navBtnProfile: ".header-link-profile",
    navBtnQuery: ".header-link-query",
    navBtnLogin: "",
    navBtnRegister: "",

    btnShowRegister: ".card.login .btn-show-register",
    btnShowLogin: ".card.register btn-show-login",

    btnQuery: ".btn-query",
    btnRegister: ".card.register .btn-register",
    btnLogin: ".card.login .btn-login",

    queryEndpoint: ".card.builder .endpoint",
    queryPayload: ".card.builder .payload",
    queryResult: ".card.builder .result",

    registerUsername: ".card.register .username",
    registerPassword: ".card.register .password",
    registerFirstname: ".card.register .firstname",
    registerLastname: ".card.register .lastname",

    loginUsername: ".card.login .username",
    loginPassword: ".card.login .password",

    loader: ".loader"
  };

  const loading = (isLoading) => (isLoading ? $(controls.loader).show() : $(controls.loader).hide());
  const hide = (...selectors) => selectors.forEach((selector) => $(selector).hide());
  const show = (...selectors) => selectors.forEach((selector) => $(selector).show());
  const bold = (...selectors) => {
    Object.values(controls).forEach((selector) => {
      if (selectors.includes(selector)) {
        $(selector).addClass("font-weight-bold");
      } else {
        $(selector).removeClass("font-weight-bold");
      }
    });
  };

  // NOTE: IDK why but without timeout `navigate` sometimes doesn't work
  const go = (route) => setTimeout(() => router.navigate(route), 100);

  const updateControlsVisibility = (page) => {
    switch (page) {
      case "login":
        hide(controls.navBtnLogout, controls.navBtnProfile, controls.navBtnQuery);
        show(controls.navBtnLogin, controls.navBtnRegister);
        bold(controls.navBtnLogin);
        break;
      case "register":
        hide(controls.navBtnLogout, controls.navBtnProfile, controls.navBtnQuery);
        show(controls.navBtnLogin, controls.navBtnRegister);
        bold(controls.navBtnRegister);
        break;
      case "query":
        hide(controls.navBtnLogin, controls.navBtnRegister);
        show(controls.navBtnLogout, controls.navBtnProfile, controls.navBtnQuery);
        bold(controls.navBtnQuery);
        break;
      case "profile":
        hide(controls.navBtnLogin, controls.navBtnRegister);
        show(controls.navBtnLogout, controls.navBtnProfile, controls.navBtnQuery);
        bold(controls.navBtnProfile);
        break;
      default:
        console.error(`Unknown page passed to updateControlsVisibility: ${page}`);
    }
  };

  const handlers = {
    handleLogout: () => {
      Cookies.remove(COOKIE_NAME);
      go("/");
    },

    handleQuery: () => {
      const [method, endpoint] = $(controls.queryEndpoint).val().split("|");
      let payload = $(controls.queryPayload).val() || "{}";

      $(controls.queryResult).html("");

      if (!method || !endpoint) {
        return;
      }

      try {
        payload = JSON.parse(payload);
      } catch (error) {
        $.toast({
          text: `Payload is not valida JSON object. Double quotes, commas and paired bramckets are important for validaty`,
          icon: "warning",
          hideAfter: 7000
        });
        return;
      }

      const opts = {
        url: apiBaseUrl + "/query/" + endpoint,
        method,
        headers: { Authorization: `Bearer ${getToken()}` }
      };

      if (method !== "GET") {
        opts.contentType = "application/json; charset=utf-8";
        opts.data = JSON.stringify(payload);
      } else {
        opts.data = payload;
      }

      loading(true);

      $.ajax(opts)
        .done((response) => {
          if (!response.success) {
            $.toast({ text: `Unable to process your request`, icon: "error" });
            return;
          }

          $(controls.queryResult).html(JSON.stringify(response.content, null, 2));
        })
        .fail((xhr, err, status) => {
          console.error("Registration error:", err, status);
          $.toast({ text: `Unable to process your request`, icon: "error" });
          handlers.logout();
        })
        .always(() => loading(false));
    },

    handleRegister: () => {
      const username = $(controls.registerUsername).val();
      const password = $(controls.registerPassword).val();
      const first_name = $(controls.registerFirstname).val();
      const last_name = $(controls.registerLastname).val();

      loading(true);

      $.ajax({
        url: apiBaseUrl + "/account/register",
        method: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ username, password, first_name, last_name })
      })
        .done((response) => {
          if (!response.success) {
            $.toast({
              text: `Unable to create account, some information missing or account already exists`,
              icon: "error"
            });
            return;
          }

          $.toast({ text: `Your account successfully registered, please login.`, icon: "success" });
        })
        .fail((xhr, err, status) => {
          console.error("Registration error:", err, status);
          Cookies.remove(COOKIE_NAME);
          $.toast({ text: `Unable to create account, some information missing`, icon: "error" });
        })
        .always(() => loading(false));
    },

    handleLogin: () => {
      const username = $(controls.loginUsername).val();
      const password = $(controls.loginPassword).val();

      loading(true);

      $.ajax({
        url: apiBaseUrl + "/account/login",
        method: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ username, password })
      })
        .done((response) => {
          token = response.token;
          queryToken = response.query_token;
          reqCount = response.req_count;

          if (!token) {
            console.error("Success but no token:", response);
            $.toast({ text: `Username or password incorrect`, icon: "error" });
          }

          if (reqCount > 0) {
            Cookies.set(COOKIE_NAME, token);
            $.toast({ text: `You successfully logged in, have ${reqCount} more API requests`, icon: "success" });
            getToken();
          } else {
            $.toast({
              text: `You successfully logged in but consumed all available API requests count!`,
              icon: "warning"
            });
          }

          go("/query");
        })
        .fail((xhr, err, status) => {
          console.error("Login error:", err);
          Cookies.remove(COOKIE_NAME);
          $.toast({ text: `Username or password incorrect`, icon: "error" });
        })
        .always(() => loading(false));
    }
  };

  $(document)
    .on("click", controls.navBtnLogout, () => {
      handlers.handleLogout();
    })
    .on("click", controls.btnQuery, () => {
      handlers.handleQuery();
    })
    .on("click", controls.btnRegister, () => {
      handlers.handleRegister();
    })
    .on("click", controls.btnLogin, () => {
      handlers.handleLogin();
    });

  router
    .on({
      "/login": function () {
        renderPage("login");
        updateControlsVisibility("login");
      },
      "/register": function () {
        renderPage("register");
        updateControlsVisibility("register");
      }
    })
    .resolve();

  router
    .on(
      "/query",
      function () {
        renderPage("builder");
        updateControlsVisibility("query");
      },
      {
        before: function (done, params) {
          if (!getToken()) {
            go("/login");
            return done(false);
          }

          done();
        }
      }
    )
    .resolve();

  router
    .on(
      "/profile",
      function () {
        renderPage("profile");
        updateControlsVisibility("profile");
      },
      {
        before: function (done, params) {
          if (!getToken()) {
            go("/login");
            return done(false);
          }

          done();
        }
      }
    )
    .resolve();

  router
    .on(() => {
      if (!getToken()) {
        hide(controls.navBtnLogout, controls.navBtnProfile);
        go("/login");
        return;
      }

      go("/query");
    })
    .resolve();

  router.resolve();

  window.router = router;
}
