function init(apiBaseUrl) {
  const COOKIE_NAME = "fam_auth_2_0_0";

  const root = null;
  const useHash = true;
  const hash = "#!";
  const router = new Navigo(root, useHash, hash);

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

    console.log(`Rendering page ${name} in element`, parent);

    parent.innerHTML = content;
  };

  const controls = {
    navBtnLogout: ".header-link-logout",
    navBtnProfile: ".header-link-profile",

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

  const handlers = {
    handleLogout: () => {
      Cookies.remove(COOKIE_NAME);
      router.navigate("/login");
    },

    handleShowProfile: () => {
      router.navigate("/profile");
    },
    handleShowRegister: () => {
      router.navigate("/register");
    },
    handleShowLogin: () => {
      router.navigate("/login");
    },

    logout: () => {
      Cookies.remove(COOKIE_NAME);
      router.navigate("/login");
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
            token = checkToken();
          } else {
            $.toast({
              text: `You successfully logged in but consumed all available API requests count!`,
              icon: "warning"
            });
            Cookies.remove(COOKIE_NAME);
          }
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
      console.log(">> click on navBtnLogout");
      handlers.handleLogout();
    })
    .on("click", controls.navBtnProfile, () => {
      console.log(">> click on navBtnProfile");
      handlers.handleShowProfile();
    })
    .on("click", controls.btnQuery, () => {
      console.log(">> click on btnQuery");
      handlers.handleQuery();
    })
    .on("click", controls.btnShowRegister, () => {
      console.log(">> click on btnShowRegister");
      handlers.handleShowRegister();
    })
    .on("click", controls.btnShowLogin, () => {
      console.log(">> click on btnShowLogin");
      handlers.handleShowLogin();
    })
    .on("click", controls.btnRegister, () => {
      console.log(">> click on btnRegister");
      handlers.handleRegister();
    })
    .on("click", controls.btnLogin, () => {
      console.log(">> click on btnLogin");
      handlers.handleLogin();
    });

  router
    .on({
      "/login": function () {
        console.log(">>> 1");
        renderPage("login");
      },
      "/register": function () {
        console.log(">>> 2");
        renderPage("register");
      },
      "/query": function () {
        renderPage("builder");
      },
      "/profile": function () {
        renderPage("profile");
      },
      "*": function () {
        if (!getToken()) {
          hide(controls.navBtnLogout, controls.navBtnProfile);
          router.navigate("/login");
          return;
        }

        router.navigate("/query");
      }
    })
    .resolve();
}
