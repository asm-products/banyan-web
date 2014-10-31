var BrowserDetect = {
  init: function() {
    this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
    this.version = this.searchVersion(navigator.userAgent) || this.searchVersion(navigator.appVersion) || "an unknown version";
    this.OS = this.searchString(this.dataOS) || "an unknown OS";
  },
  searchString: function(data) {
    for (var i = 0; i < data.length; i++) {
      var dataString = data[i].string;
      var dataProp = data[i].prop;
      this.versionSearchString = data[i].versionSearch || data[i].identity;
      if (dataString) {
        if (dataString.indexOf(data[i].subString) != -1) {
          return data[i].identity;
        }
      } else {
        if (dataProp) {
          return data[i].identity;
        }
      }
    }
  },
  searchVersion: function(dataString) {
    var index = dataString.indexOf(this.versionSearchString);
    if (index == -1) {
      return;
    }
    return parseFloat(dataString.substring(index + this.versionSearchString.length + 1));
  },
  dataBrowser: [{
    string: navigator.userAgent,
    subString: "Chrome",
    identity: "Chrome"
  }, {
    string: navigator.userAgent,
    subString: "OmniWeb",
    versionSearch: "OmniWeb/",
    identity: "OmniWeb"
  }, {
    string: navigator.vendor,
    subString: "Apple",
    identity: "Safari",
    versionSearch: "Version"
  }, {
    prop: window.opera,
    identity: "Opera"
  }, {
    string: navigator.vendor,
    subString: "iCab",
    identity: "iCab"
  }, {
    string: navigator.vendor,
    subString: "KDE",
    identity: "Konqueror"
  }, {
    string: navigator.userAgent,
    subString: "Firefox",
    identity: "Firefox"
  }, {
    string: navigator.vendor,
    subString: "Camino",
    identity: "Camino"
  }, {
    string: navigator.userAgent,
    subString: "Netscape",
    identity: "Netscape"
  }, {
    string: navigator.userAgent,
    subString: "MSIE",
    identity: "Explorer",
    versionSearch: "MSIE"
  }, {
    string: navigator.userAgent,
    subString: "Gecko",
    identity: "Mozilla",
    versionSearch: "rv"
  }, {
    string: navigator.userAgent,
    subString: "Mozilla",
    identity: "Netscape",
    versionSearch: "Mozilla"
  }],
  dataOS: [{
    string: navigator.platform,
    subString: "Win",
    identity: "Windows"
  }, {
    string: navigator.platform,
    subString: "Mac",
    identity: "Mac"
  }, {
    string: navigator.userAgent,
    subString: "iPhone",
    identity: "iPhone/iPod"
  }, {
    string: navigator.platform,
    subString: "Linux",
    identity: "Linux"
  }]
};
BrowserDetect.init();
var TT = TT || {};
TT.PAGE_WIDTH = 800;
TT.PAGE_HEIGHT = 500;
TT.PAGE_MIN_WIDTH = 1000;
TT.PAGE_MIN_HEIGHT = 680;
TT.PAGE_MARGIN_X = 32;
TT.PAGE_MARGIN_Y = 10;
TT.BOOK_WIDTH = 1660;
TT.BOOK_HEIGHT = 520;
TT.BOOK_WIDTH_CLOSED = TT.BOOK_WIDTH / 2;
TT.BOOK_OFFSET_X = 5;
TT.UA = navigator.userAgent.toLowerCase();
TT.initialize = function() {
  TT.preloader.initialize();
  TT.overlay.initialize();
  TT.storage.initialize();
  TT.cache.initialize();
  TT.search.initialize();
  TT.chapternav.initialize();
  TT.sharing.initialize();
  TT.paperstack.initialize();
  TT.tableofthings.initialize();
  TT.flipintro.initialize();
  $(window).resize(TT.onWindowResize);
  $(window).scroll(TT.onWindowScroll);
  TT.updateLayout();
  $("img").mousedown(function(event) {
    event.preventDefault();
  });
};
TT.startup = function() {
  TT.navigation.initialize();
  TT.pageflip.initialize();
  TT.history.initialize();
  TT.locale.initialize();
  TT.chapternav.updateSelection();
  TT.tableofthings.updateSelection();
  TT.chapternav.updateReadMarkers();
  TT.tableofthings.updateReadMarkers();
  TT.paperstack.updateStack();
  TT.navigation.updateNextPrevLinks($("#pages section.current"));
};
TT.onWindowResize = function(event) {
  TT.updateLayout();
};
TT.onWindowScroll = function(event) {
  TT.updateLayout(true);
};
TT.updateLayout = function(fromScroll) {
  var applicationSize = {
    width: $(window).width(),
    height: $(window).height()
  };
  $("body").css({
    overflowX: applicationSize.width < TT.PAGE_MIN_WIDTH ? "auto" : "hidden",
    overflowY: applicationSize.height < TT.PAGE_MIN_HEIGHT ? "auto" : "hidden"
  });
  applicationSize.width = Math.max(applicationSize.width, TT.PAGE_MIN_WIDTH);
  applicationSize.height = Math.max(applicationSize.height, TT.PAGE_MIN_HEIGHT);
  var center = {
    x: applicationSize.width * 0.5,
    y: applicationSize.height * 0.5
  };
  if (!fromScroll) {
    if (applicationSize.width < TT.PAGE_MIN_WIDTH + $("#grey-mask").width() + 50) {
      $("#grey-mask").css({
        left: -((TT.PAGE_MIN_WIDTH + $("#grey-mask").width() + 50) - applicationSize.width)
      });
    } else {
      $("#grey-mask").css({
        left: 0
      });
    }
    $("#book").css({
      left: center.x - (TT.BOOK_WIDTH * 0.5) - (TT.BOOK_WIDTH_CLOSED * 0.5) + TT.BOOK_OFFSET_X,
      top: center.y - (TT.BOOK_HEIGHT * 0.5),
      margin: 0
    });
  }
  $("#pagination-prev, #pagination-next").css({
    top: center.y - 20
  });
  if (!TT.IS_TOUCH_DEVICE) {
    $("#pagination-prev").css({
      left: $(window).scrollLeft()
    });
    $("#pagination-next").css({
      right: "auto",
      left: $(window).scrollLeft() + $(window).width() - $("#pagination-next").width()
    });
  }
};
TT.log = function(o) {
  if (window.console && o) {
    window.console.log(o);
  }
};
TT.time = function() {
  return new Date().getTime();
};
TT.track = function(url) {	
   return;
  _gaq.push(["_trackPageview", url]);
};
window.TT = TT;
TT.preloader = {};
TT.preloader.assetsComplete = false;
TT.preloader.contentsComplete = false;
TT.preloader.finished = false;
TT.preloader.assetsLoaded = 0;
TT.preloader.assetsToLoad = 0;
TT.preloader.initialize = function() {
  TT.preloader.animation.initialize();
  TT.preloader.animation.activate();
  TT.preloader.assetsToLoad = 9;
  var spritesImage = new Image();
  var frontImage = new Image();
  var backImage = new Image();
  var rightImage = new Image();
  var leftImage = new Image();
  var repeatImage = new Image();
  var paperImage = new Image();
  var leftFlippedImage = new Image();
  var backImageFlipped = new Image();
  TT.preloader.addAssetToPreloadQueue($(spritesImage));
  TT.preloader.addAssetToPreloadQueue($(frontImage));
  TT.preloader.addAssetToPreloadQueue($(backImage));
  TT.preloader.addAssetToPreloadQueue($(rightImage));
  TT.preloader.addAssetToPreloadQueue($(leftImage));
  TT.preloader.addAssetToPreloadQueue($(repeatImage));
  TT.preloader.addAssetToPreloadQueue($(paperImage));
  TT.preloader.addAssetToPreloadQueue($(leftFlippedImage));
  TT.preloader.addAssetToPreloadQueue($(backImageFlipped));
  $("#preloader .contents").delay(50).animate({
    opacity: 1
  }, 300);

  var bookDirectory = "book/";
  spritesImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "sprites.png";
  frontImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "front-cover.jpg";
  backImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "back-cover.jpg";
  rightImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "right-page.jpg";
  leftImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "left-page.jpg";
  repeatImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "repeat-x.png";
  paperImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "right-page-paper.jpg";
  leftFlippedImage.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "left-page-flipped.jpg";
  backImageFlipped.src = SERVER_VARIABLES.STATIC_IMAGES + bookDirectory + "back-cover-flipped.jpg";
};
TT.preloader.updateMeter = function() {
  var segmentsTotal = TT.preloader.assetsToLoad;
  var segmentsComplete = TT.preloader.assetsLoaded;
  if (TT.preloader.contentsComplete) {
    segmentsComplete++;
  }
  var progress = Math.min(segmentsComplete / segmentsTotal, 1);
  var progressWidth = progress * $("#preloader .progress").width();
  $("#preloader .progress .fill").width(progressWidth);
};
TT.preloader.addAssetToPreloadQueue = function(asset) {
  asset.load(TT.preloader.onAssetLoaded);
  asset.error(TT.preloader.onAssetLoaded);
};
TT.preloader.onAssetLoaded = function(event) {
  if (++TT.preloader.assetsLoaded >= TT.preloader.assetsToLoad) {
    TT.preloader.onAllAssetsLoaded();
  }
  TT.log("Asset preloaded: " + $(event.target).attr("src") + " [" + TT.preloader.assetsLoaded + "/" + TT.preloader.assetsToLoad + "]");
  TT.preloader.updateMeter();
};
TT.preloader.onAllAssetsLoaded = function() {
  if (!TT.preloader.assetsComplete && TT.preloader.assetsLoaded >= TT.preloader.assetsToLoad) {
    TT.preloader.assetsComplete = true;
    TT.preloader.finish();
  }
  TT.preloader.updateMeter();
};
TT.preloader.onContentsLoaded = function() {
  if (!TT.preloader.contentsComplete) {
    TT.preloader.contentsComplete = true;
    TT.preloader.finish();
  }
  TT.preloader.updateMeter();
};
TT.preloader.finish = function() {
  if (TT.preloader.contentsComplete && TT.preloader.assetsComplete && !TT.preloader.finished) {
    $("#preloader").stop(true, true).fadeOut(200, function() {
      TT.preloader.animation.deactivate();
      $(this).remove();
    });
    $("#book").css({
      opacity: 0
    }).show().delay(200).fadeTo(700, 1);
    TT.updateLayout();
    TT.startup();
    setTimeout(TT.preloader.loadIllustrations, 3000);
    TT.preloader.finished = true;
  }
  TT.preloader.updateMeter();
};
TT.preloader.loadIllustrations = function() {
  $("div.page").find("img").each(function() {
    if ($(this).attr("src") !== $(this).attr("data-src")) {
      $(this).attr("src", $(this).attr("data-src"));
    }
  });
};
TT.preloader.animation = {};
TT.preloader.animation.loopInterval = -1;
TT.preloader.animation.WIDTH = 89;
TT.preloader.animation.HEIGHT = 29;
TT.preloader.animation.VSPACE = 20;
TT.preloader.animation.canvas = null;
TT.preloader.animation.context = null;
TT.preloader.animation.flip = {
  progress: 0,
  alpha: 0
};
TT.preloader.animation.initialize = function() {
  this.canvas = $("#preloader .animation");
  if (this.canvas[0]) {
    this.canvas[0].width = this.WIDTH;
    this.canvas[0].height = this.HEIGHT + (this.VSPACE * 2);
    this.context = this.canvas[0].getContext("2d");
  }
};
TT.preloader.animation.activate = function() {
  if (TT.preloader.animation.loopInterval == -1) {
    TT.preloader.animation.flip.progress = 1;
    TT.preloader.animation.loopInterval = setInterval(function() {
      if (TT.preloader.animation.canvas[0]) {
        TT.preloader.animation.render();
      }
    }, 32);
  }
};
TT.preloader.animation.deactivate = function() {
  clearInterval(TT.preloader.animation.loopInterval);
  TT.preloader.animation.loopInterval = -1;
};
TT.preloader.animation.render = function() {
  this.context.clearRect(0, 0, this.WIDTH, this.HEIGHT + (this.VSPACE * 2));
  this.context.save();
  this.context.translate(0, this.VSPACE);
  this.context.fillStyle = "#f4f4f4";
  this.context.fillRect(0, 0, this.WIDTH, this.HEIGHT);
  this.context.fillStyle = "#999999";
  this.context.fillRect(0, 0, this.WIDTH, 1);
  this.context.fillRect(0, this.HEIGHT, this.WIDTH, 2);
  this.context.fillRect(0, 0, 1, this.HEIGHT);
  this.context.fillRect(this.WIDTH - 1, 0, 1, this.HEIGHT);
  this.context.fillRect(Math.floor(this.WIDTH * 0.5), 0, 1, this.HEIGHT);
  this.context.fillRect(54, 8, 25, 2);
  this.context.fillRect(54, 11, 25, 2);
  this.context.fillRect(54, 14, 25, 2);
  this.context.fillRect(54, 17, 25, 2);
  this.context.fillRect(54, 20, 25, 2);
  this.context.translate(0, 1);
  TT.preloader.animation.flip.progress -= Math.max(0.12 * (1 - Math.abs(TT.preloader.animation.flip.progress)), 0.02);
  TT.preloader.animation.flip.alpha = 1 - ((Math.abs(TT.preloader.animation.flip.progress) - 0.7) / 0.3);
  if (TT.preloader.animation.flip.progress <= -1.1) {
    TT.preloader.animation.flip.progress = 1;
  }
  var strength = 1 - Math.abs(TT.preloader.animation.flip.progress);
  var anchorOutdent = strength * 12;
  var controlOutdent = strength * 8;
  var source = {
    top: {
      x: this.WIDTH * 0.5,
      y: 0
    },
    bottom: {
      x: this.WIDTH * 0.5,
      y: this.HEIGHT
    }
  };
  var destination = {
    top: {
      x: source.top.x + (this.WIDTH * TT.preloader.animation.flip.progress * 0.55),
      y: 0 - anchorOutdent
    },
    bottom: {
      x: source.bottom.x + (this.WIDTH * TT.preloader.animation.flip.progress * 0.55),
      y: this.HEIGHT - anchorOutdent
    }
  };
  var control = {
    top: {
      x: source.top.x + (12 * TT.preloader.animation.flip.progress),
      y: -controlOutdent
    },
    bottom: {
      x: source.bottom.x + (12 * TT.preloader.animation.flip.progress),
      y: this.HEIGHT - controlOutdent
    }
  };
  this.context.fillStyle = "rgba(245,245,245," + TT.preloader.animation.flip.alpha + ")";
  this.context.strokeStyle = "rgba(90,90,90," + TT.preloader.animation.flip.alpha + ")";
  this.context.beginPath();
  this.context.moveTo(source.top.x, source.top.y);
  this.context.quadraticCurveTo(control.top.x, control.top.y, destination.top.x, destination.top.y);
  this.context.lineTo(destination.bottom.x, destination.bottom.y);
  this.context.quadraticCurveTo(control.bottom.x, control.bottom.y, source.bottom.x, source.bottom.y);
  this.context.fill();
  this.context.stroke();
  this.context.restore();
};
TT.history = {};
TT.history.TABLE_OF_CONTENTS = "table-of-things";
TT.history.HOME = "home";
TT.history.FOREWORD = "foreword";
TT.history.THEEND = "theend";
TT.history.CREDITS = "credits";
TT.history.previousHash = "";
TT.history.hashCheckInterval = -1;
TT.history.STORY = "story";
TT.history.storyId;

TT.history.initialize = function() {
  if (TT.history.supportsHistoryPushState()) {
    $(window).bind("popstate", TT.history.onPopState);
  } else {
    TT.history.hashCheckInterval = setInterval(TT.history.onCheckHash, 200);
  }
};
TT.history.supportsHistoryPushState = function() {
  return ("pushState" in window.history) && window.history.pushState !== null;
};
TT.history.onCheckHash = function() {
  if (document.location.hash !== TT.history.previousHash) {
    TT.history.navigateToPath(document.location.hash.slice(1));
    TT.history.previousHash = document.location.hash;
  }
};
TT.history.pushState = function(url) {
  url = "/" + TT.history.STORY + "/" + TT.history.storyId + url;	
  if (TT.history.supportsHistoryPushState()) {
  	try{
  		window.history.pushState("", "", url);
  	} catch(e) {
  		TT.log(e);
  	}
    
  } else {
    TT.history.previousHash = "#" + url;
    document.location.hash = url;
  }
  TT.track(url);
};
TT.history.onPopState = function(event) {
  TT.history.navigateToPath(document.location.pathname);
};
TT.history.navigateToPath = function(pathname) {
  // pathname = TT.locale.removeLocaleCodeFromURL(pathname);
  var part1 = pathname.split("/")[1]; // "story"
  var part2 = pathname.split("/")[2]; // storyId
  var part3 = pathname.split("/")[3]; // *
  var part4 = pathname.split("/")[4]; // pieceId
  if (part1 == TT.history.STORY || part1 == "Users") {
  	TT.history.storyId = part2;
  } else {
  	alert("This is a wrong url to work with!!");
  }
  
  if (!part3 || part3 == TT.history.HOME) {
    TT.navigation.goToHome(true);
  } else {
    if (part3 == TT.history.CREDITS) {
      TT.navigation.goToCredits(true);
    } else {
      if (part3 == TT.history.TABLE_OF_CONTENTS) {
        TT.tableofthings.show();
      } else {
        if (part2) {
          TT.navigation.goToPage(part3, part4, true);
        } else {
          TT.navigation.goToPage(part3, "1", true);
        }
      }
    }
  }
};
TT.storage = {};
TT.storage.isFirstTimeVisitor = true;
TT.storage.contents = "";
TT.storage.data = {
  articles: {},
  progress: {},
  bookmark: {
    articleId: "",
    pageNumber: ""
  }
};
TT.storage.initialize = function() {
  TT.storage.routeDataRequest();
};
TT.storage.load = function() {
  if (TT.storage.supportsLocalStorage() && localStorage.data) {
    TT.storage.data = $.parseJSON(localStorage.data);
  }
};
TT.storage.save = function() {
  if (TT.storage.supportsLocalStorage()) {
    localStorage.data = $.toJSON(TT.storage.data);
  }
};
TT.storage.supportsLocalStorage = function() {
  return ("localStorage" in window) && window.localStorage !== null;
};
TT.storage.getArticlesFromServer = function() {
  TT.log("Getting articles from server");
  var disabledArticles = TT.chapternav.getDisabledArticles();
  // $.ajax({
    // url: "/" + SERVER_VARIABLES.LANG + "/all",
    // contentType: "text/html;charset=UTF-8",
    // success: function(data) {
      var book = document.getElementById("book");
      var globalPageCounter = 0;
      TT.storage.data.articles = {};
      $(book).each(function() {
        var articleId = $(this).attr("id");
        $(this).find("section").each(function(i) {
          globalPageCounter++;
          $(this).addClass("globalPage-" + globalPageCounter).css("zIndex", 500 - globalPageCounter).hide();
          $(this).addClass("title-piece");
          $(this).addClass("page-" + globalPageCounter);
        });
      });
      // TT.storage.save();
      // TT.storage.onFindBookmark();
      TT.storage.activateCurrentPageAndSetPageCount();
    // }
  // });
};

TT.storage.getArticlesFromStorage = function() {
  TT.log("Getting articles from storage");
  TT.storage.isFirstTimeVisitor = false;
  if (localStorage.data) {
    TT.storage.data = $.parseJSON(localStorage.data);
  } else {
    TT.storage.getArticlesFromServer();
    return;
  }
  var disabledArticles = TT.chapternav.getDisabledArticles();
  for (var articlePath in TT.storage.data.articles) {
    var articleIsDisabled = false;
    for (var i = 0; i < disabledArticles.length; i++) {
      if (disabledArticles[i] == articlePath.split("/")[1]) {
        articleIsDisabled = true;
      }
    }
    if (articleIsDisabled == false) {
      $("#pages").append(TT.storage.data.articles[articlePath]);
    }
  }
  TT.storage.onFindBookmark();
  TT.storage.activateCurrentPageAndSetPageCount();
};
TT.storage.routeDataRequest = function() {
	TT.storage.getArticlesFromServer();
};
TT.storage.activateCurrentPageAndSetPageCount = function() {
  var $origArticle = $("#pages section").eq(0);
  $origArticle.attr("id", "original");
  $("#pages section:not(#original)").each(function(i) {
    if ($(this).hasClass($origArticle.attr("class"))) {
      $origArticle.remove();
      $(this).addClass("current").show().next("section").show();
      $('<span id="currentPage">' + parseFloat(i + 1) + "</span>").appendTo("body");
    }
  });
  if ($("#pages section.current").length === 0) {
    $("#pages section").first().addClass("current");
  }
  $("#pages section div.page").each(function(i) {
    $(this).append('<span class="pageNumber">' + (i + 1) + "</span>");
  });
  if ($("body").hasClass("home")) {
    $("#pages section").removeClass("current");
    $("#pages section").first().addClass("current");
  } else {
    if ($("body").hasClass("credits")) {
      $("#pages section").removeClass("current");
      $("#pages section").last().addClass("current");
    }
  }
  TT.preloader.onContentsLoaded();
};

TT.storage.hasArticleBeenRead = function(articleId) {
  return TT.storage.data.progress["/" + articleId + "/1"] == true;
};
TT.pageflip = {};
TT.pageflip.HINT_WIDTH = 100;
TT.pageflip.HINT_WIDTH_TOUCH = 250;
TT.pageflip.CANVAS_VERTICAL_PADDING = 80;
TT.pageflip.CANVAS_HORIZONTAL_PADDING = 20;
TT.pageflip.CANVAS_WIDTH = TT.BOOK_WIDTH + (TT.pageflip.CANVAS_HORIZONTAL_PADDING * 2);
TT.pageflip.CANVAS_HEIGHT = TT.BOOK_HEIGHT + (TT.pageflip.CANVAS_VERTICAL_PADDING * 2);
TT.pageflip.FRAMERATE = 30;
TT.pageflip.CLICK_FREQUENCY = 350;
TT.pageflip.SOFT_FLIP = "soft";
TT.pageflip.HARD_FLIP = "hard";
TT.pageflip.pages = [];
TT.pageflip.flips = [];
TT.pageflip.canvas = null;
TT.pageflip.context = null;
TT.pageflip.dirtyRegion = new Region();
TT.pageflip.dragging = false;
TT.pageflip.turning = false;
TT.pageflip.hinting = false;
TT.pageflip.loopInterval = -1;
TT.pageflip.mouse = {
  x: 0,
  y: 0,
  down: false
};
TT.pageflip.mouseHistory = [];
TT.pageflip.skew = {
  top: 0,
  topTarget: 0,
  bottom: 0,
  bottomTarget: 0
};
TT.pageflip.mouseDownTime = 0;
TT.pageflip.texture = null;
TT.pageflip.textures = {};
TT.pageflip.flippedLeftPage = null;
TT.pageflip.flippedBackCover = null;
TT.pageflip.lastKeyboardNavigationTime = 0;
TT.pageflip.lastKeyboardNavigationDirection = null;
TT.pageflip.eventsAreBound = null;
TT.pageflip.initialize = function() {
  TT.pageflip.createCanvas();
  TT.pageflip.createTextures();
  if (TT.pageflip.eventsAreBound == null) {
    TT.pageflip.registerEventListeners();
  }
  $(document).bind("keydown", TT.pageflip.onKeyPress);
};
TT.pageflip.registerEventListeners = function() {
  TT.pageflip.unregisterEventListeners();
  TT.pageflip.eventsAreBound = true;
  $(document).bind("mousemove", TT.pageflip.onMouseMove);
  $(document).bind("mousedown", TT.pageflip.onMouseDown);
  $(document).bind("mouseup", TT.pageflip.onMouseUp);
  if (TT.IS_TOUCH_DEVICE) {
    document.addEventListener("touchstart", TT.pageflip.onTouchStart, false);
    document.addEventListener("touchmove", TT.pageflip.onTouchMove, false);
    document.addEventListener("touchend", TT.pageflip.onTouchEnd, false);
  }
};
TT.pageflip.unregisterEventListeners = function() {
  TT.pageflip.eventsAreBound = false;
  $(document).unbind("mousemove", TT.pageflip.onMouseMove);
  $(document).unbind("mousedown", TT.pageflip.onMouseDown);
  $(document).unbind("mouseup", TT.pageflip.onMouseUp);
  if (TT.IS_TOUCH_DEVICE) {
    document.removeEventListener("touchstart", TT.pageflip.onTouchStart);
    document.removeEventListener("touchmove", TT.pageflip.onTouchMove);
    document.removeEventListener("touchend", TT.pageflip.onTouchEnd);
  }
};
TT.pageflip.createTextures = function() {
  TT.pageflip.flippedLeftPage = $("<img>", {
    src: $("#left-page img").attr("data-src-flipped"),
    width: $("#left-page img").attr("width"),
    height: $("#left-page img").attr("height")
  })[0];
  TT.pageflip.flippedBackCover = $("<img>", {
    src: $("#back-cover img").attr("data-src-flipped"),
    width: $("#back-cover img").attr("width"),
    height: $("#back-cover img").attr("height")
  })[0];
  TT.pageflip.textures.front = $("#front-cover img")[0];
  TT.pageflip.textures.back = TT.pageflip.flippedBackCover;
  TT.pageflip.textures.left = TT.pageflip.flippedLeftPage;
  TT.pageflip.textures.right = $("#right-page img")[0];
};
TT.pageflip.createCanvas = function() {
  TT.pageflip.canvas = $('<canvas id="pageflip"></canvas>');
  TT.pageflip.canvas.css({
    position: "absolute",
    top: -TT.pageflip.CANVAS_VERTICAL_PADDING,
    left: -TT.pageflip.CANVAS_HORIZONTAL_PADDING,
    zIndex: 0
  });
  TT.pageflip.canvas[0].width = TT.pageflip.CANVAS_WIDTH;
  TT.pageflip.canvas[0].height = TT.pageflip.CANVAS_HEIGHT;
  TT.pageflip.context = TT.pageflip.canvas[0].getContext("2d");
  TT.pageflip.canvas.appendTo($("#book"));
};
TT.pageflip.createCanvasTexture = function(image, translation, scale, rotation) {
  var canvas = $("<canvas></canvas>");
  canvas.css({
    position: "absolute",
    display: "block"
  });
  canvas[0].width = TT.BOOK_WIDTH_CLOSED;
  canvas[0].height = TT.BOOK_HEIGHT;
  var context = canvas[0].getContext("2d");
  context.translate(translation.x, translation.y);
  context.scale(scale.x, scale.y);
  context.rotate(rotation);
  context.drawImage(image, 0, 0);
  return canvas[0];
};
TT.pageflip.activate = function() {
  if (TT.pageflip.loopInterval == -1) {
    clearInterval(TT.pageflip.loopInterval);
    TT.pageflip.loopInterval = setInterval(TT.pageflip.redraw, 1000 / TT.pageflip.FRAMERATE);
  }
  TT.pageflip.canvas.css("z-index", 1010);
};
TT.pageflip.deactivate = function() {
  clearInterval(TT.pageflip.loopInterval);
  TT.pageflip.loopInterval = -1;
  TT.pageflip.context.clearRect(0, 0, TT.pageflip.CANVAS_WIDTH, TT.pageflip.CANVAS_HEIGHT);
  TT.pageflip.canvas.css("z-index", 0);
};
TT.pageflip.redraw = function() {
  var cvs = TT.pageflip.canvas[0];
  var ctx = TT.pageflip.context;
  var dirtyRect = TT.pageflip.dirtyRegion.toRectangle(40);
  if (dirtyRect.width > 1 && dirtyRect.height > 1) {
    ctx.clearRect(dirtyRect.x, dirtyRect.y, dirtyRect.width, dirtyRect.height);
  }
  TT.pageflip.dirtyRegion.reset();
  for (var i = 0, len = TT.pageflip.flips.length; i < len; i++) {
    var flip = TT.pageflip.flips[i];
    if (flip.type == TT.pageflip.HARD_FLIP) {
      TT.pageflip.renderHardFlip(flip);
    } else {
      TT.pageflip.renderSoftFlip(flip);
    }
  }
  TT.pageflip.removeInactiveFlips();
};
TT.pageflip.renderSoftFlip = function(flip) {
  var mouse = TT.pageflip.mouse;
  var skew = TT.pageflip.skew;
  var cvs = TT.pageflip.canvas[0];
  var ctx = TT.pageflip.context;
  var currentPage = flip.currentPage;
  if (flip.direction === -1) {
    currentPage = flip.targetPage;
  } else {
    flip.targetPage.width(TT.PAGE_WIDTH);
  }
  if (TT.pageflip.dragging && !flip.consumed) {
    mouse.x = Math.max(Math.min(mouse.x, TT.PAGE_WIDTH), -TT.PAGE_WIDTH);
    mouse.y = Math.max(Math.min(mouse.y, TT.PAGE_HEIGHT), 0);
    flip.progress = Math.min(mouse.x / TT.PAGE_WIDTH, 1);
  } else {
    var distance = Math.abs(flip.target - flip.progress);
    var speed = flip.target == -1 ? 0.3 : 0.2;
    var ease = distance < 1 ? speed + Math.abs(flip.progress * (1 - speed)) : speed;
    ease *= Math.max(1 - Math.abs(flip.progress), flip.target == 1 ? 0.5 : 0.2);
    flip.progress += (flip.target - flip.progress) * ease;
    if (Math.round(flip.progress * 99) == Math.round(flip.target * 99)) {
      flip.progress = flip.target;
      flip.x = TT.PAGE_WIDTH * flip.progress;
      currentPage.css({
        width: flip.x
      });
      if (flip.target == 1 || flip.target == -1) {
        flip.consumed = true;
        TT.pageflip.completeCurrentTurn();
        return false;
      }
    }
  }
  flip.x = TT.PAGE_WIDTH * flip.progress;
  flip.strength = 1 - (flip.x / TT.PAGE_WIDTH);
  if (flip.target == -1 && flip.progress < -0.9) {
    flip.alpha = 1 - ((Math.abs(flip.progress) - 0.9) / 0.1);
  }
  var shadowAlpha = Math.min(1 - ((Math.abs(flip.progress) - 0.75) / 0.25), 1);
  var centralizedFoldStrength = flip.strength > 1 ? 2 - flip.strength : flip.strength;
  var verticalOutdent = 40 * centralizedFoldStrength;
  var horizontalSpread = (TT.PAGE_WIDTH * 0.5) * flip.strength * 0.95;
  if (flip.x + horizontalSpread < 0) {
    horizontalSpread = Math.abs(flip.x);
  }
  if (TT.navigation.isCreditsPage()) {
    horizontalSpread = 0;
  }
  var shadowSpread = (TT.PAGE_WIDTH * 0.5) * Math.max(Math.min(flip.strength, 0.5), 0);
  var rightShadowWidth = (TT.PAGE_WIDTH * 0.5) * Math.max(Math.min(flip.strength, 0.5), 0);
  var leftShadowWidth = (TT.PAGE_WIDTH * 0.5) * Math.max(Math.min(centralizedFoldStrength, 0.5), 0);
  var foldShadowWidth = (TT.PAGE_WIDTH * 0.9) * Math.max(Math.min(flip.strength, 0.05), 0);
  currentPage.css({
    width: Math.max(flip.x + horizontalSpread * 0.5, 0)
  });
  if (TT.pageflip.dragging) {
    skew.topTarget = Math.max(Math.min((mouse.y / (TT.PAGE_HEIGHT * 0.5)), 1), 0) * (40 * centralizedFoldStrength);
    skew.bottomTarget = Math.max(Math.min(1 - (mouse.y - (TT.PAGE_HEIGHT * 0.5)) / (TT.PAGE_HEIGHT * 0.5), 1), 0) * (40 * centralizedFoldStrength);
  } else {
    skew.topTarget = 0;
    skew.bottomTarget = 0;
  }
  if (flip.progress === 1) {
    skew.top = 0;
    skew.bottom = 0;
  }
  skew.top += (skew.topTarget - skew.top) * 0.3;
  skew.bottom += (skew.bottomTarget - skew.bottom) * 0.3;
  flip.x += horizontalSpread;
  var drawingOffset = {
    x: TT.pageflip.CANVAS_HORIZONTAL_PADDING + TT.PAGE_MARGIN_X + TT.PAGE_WIDTH,
    y: TT.pageflip.CANVAS_VERTICAL_PADDING + TT.PAGE_MARGIN_Y
  };
  ctx.save();
  ctx.translate(drawingOffset.x, drawingOffset.y);
  ctx.globalAlpha = flip.alpha;
  if (flip.direction == -1) {
    ctx.globalCompositeOperation = "destination-over";
  }
  ctx.strokeStyle = "rgba(0,0,0,0.1)";
  ctx.lineWidth = 0.5;
  ctx.beginPath();
  ctx.moveTo(flip.x + 1, 0);
  ctx.lineTo(flip.x + 1, TT.PAGE_HEIGHT);
  ctx.stroke();
  var foldGradient = ctx.createLinearGradient(flip.x - shadowSpread, 0, flip.x, 0);
  foldGradient.addColorStop(0.35, "#fafafa");
  foldGradient.addColorStop(0.73, "#eeeeee");
  foldGradient.addColorStop(0.9, "#fafafa");
  foldGradient.addColorStop(1, "#e2e2e2");
  ctx.fillStyle = foldGradient;
  ctx.strokeStyle = "rgba(0,0,0,0.1)";
  ctx.lineWidth = 0.5;
  ctx.beginPath();
  ctx.moveTo(flip.x, 0);
  ctx.lineTo(flip.x, TT.PAGE_HEIGHT);
  ctx.quadraticCurveTo(flip.x, TT.PAGE_HEIGHT + (verticalOutdent * 1.9), flip.x - horizontalSpread + skew.bottom, TT.PAGE_HEIGHT + verticalOutdent);
  ctx.lineTo(flip.x - horizontalSpread + skew.top, -verticalOutdent);
  ctx.quadraticCurveTo(flip.x, -verticalOutdent * 1.9, flip.x, 0);
  ctx.fill();
  ctx.stroke();
  ctx.beginPath();
  ctx.strokeStyle = "rgba(0,0,0," + (0.04 * shadowAlpha) + ")";
  ctx.lineWidth = 20 * shadowAlpha;
  ctx.beginPath();
  ctx.moveTo(flip.x + skew.top - horizontalSpread, -verticalOutdent * 0.5);
  ctx.lineTo(flip.x + skew.bottom - horizontalSpread, TT.PAGE_HEIGHT + (verticalOutdent * 0.5));
  ctx.stroke();
  var rightShadowGradient = ctx.createLinearGradient(flip.x, 0, flip.x + rightShadowWidth, 0);
  rightShadowGradient.addColorStop(0, "rgba(0,0,0," + (shadowAlpha * 0.1) + ")");
  rightShadowGradient.addColorStop(0.8, "rgba(0,0,0,0.0)");
  ctx.save();
  ctx.globalCompositeOperation = "destination-over";
  ctx.fillStyle = rightShadowGradient;
  ctx.beginPath();
  ctx.moveTo(flip.x, 0);
  ctx.lineTo(flip.x + rightShadowWidth, 0);
  ctx.lineTo(flip.x + rightShadowWidth, TT.PAGE_HEIGHT);
  ctx.lineTo(flip.x, TT.PAGE_HEIGHT);
  ctx.fill();
  var foldShadowGradient = ctx.createLinearGradient(flip.x, 0, flip.x + foldShadowWidth, 0);
  foldShadowGradient.addColorStop(0, "rgba(0,0,0," + (shadowAlpha * 0.15) + ")");
  foldShadowGradient.addColorStop(1, "rgba(0,0,0,0.0)");
  ctx.fillStyle = foldShadowGradient;
  ctx.beginPath();
  ctx.moveTo(flip.x, 0);
  ctx.lineTo(flip.x + foldShadowWidth, 0);
  ctx.lineTo(flip.x + foldShadowWidth, TT.PAGE_HEIGHT);
  ctx.lineTo(flip.x, TT.PAGE_HEIGHT);
  ctx.fill();
  ctx.restore();
  var leftShadowGradient = ctx.createLinearGradient(flip.x - horizontalSpread - leftShadowWidth, 0, flip.x - horizontalSpread, 0);
  leftShadowGradient.addColorStop(0, "rgba(0,0,0,0.0)");
  leftShadowGradient.addColorStop(1, "rgba(0,0,0," + (shadowAlpha * 0.05) + ")");
  ctx.fillStyle = leftShadowGradient;
  ctx.beginPath();
  ctx.moveTo(flip.x - horizontalSpread + skew.top - leftShadowWidth, 0);
  ctx.lineTo(flip.x - horizontalSpread + skew.top, 0);
  ctx.lineTo(flip.x - horizontalSpread + skew.bottom, TT.PAGE_HEIGHT);
  ctx.lineTo(flip.x - horizontalSpread + skew.bottom - leftShadowWidth, TT.PAGE_HEIGHT);
  ctx.fill();
  ctx.restore();
  TT.pageflip.dirtyRegion.inflate(TT.PAGE_WIDTH + TT.pageflip.CANVAS_HORIZONTAL_PADDING + flip.x - horizontalSpread - leftShadowWidth, 0);
  TT.pageflip.dirtyRegion.inflate(TT.PAGE_WIDTH + TT.pageflip.CANVAS_HORIZONTAL_PADDING + flip.x + rightShadowWidth, TT.pageflip.CANVAS_HEIGHT);
};
TT.pageflip.renderHardFlip = function(flip) {
  var mouse = TT.pageflip.mouse;
  var skew = TT.pageflip.skew;
  var cvs = TT.pageflip.canvas[0];
  var ctx = TT.pageflip.context;
  var currentPage = flip.currentPage;
  if (flip.direction === -1) {
    currentPage = flip.targetPage;
  }
  if (TT.pageflip.dragging) {
    mouse.x = Math.max(Math.min(mouse.x, TT.PAGE_WIDTH), -TT.PAGE_WIDTH);
    mouse.y = Math.max(Math.min(mouse.y, TT.PAGE_HEIGHT), 0);
    flip.target = mouse.x / TT.PAGE_WIDTH;
    flip.progress += (flip.target - flip.progress) * 0.4;
  } else {
    if (Math.abs(flip.target) === 1) {
      flip.progress += Math.max(0.5 * (1 - Math.abs(flip.progress)), 0.02) * (flip.target < flip.progress ? -1 : 1);
      flip.progress = Math.max(Math.min(flip.progress, 1), -1);
    } else {
      flip.progress += (flip.target - flip.progress) * 0.4;
    }
    if (flip.progress === 1 || flip.progress === -1) {
      flip.progress = flip.target;
      flip.x = TT.PAGE_WIDTH * flip.progress;
      if (TT.navigation.isCreditsPage()) {
        currentPage.width(flip.x);
      }
      if (flip.target == 1 || flip.target == -1) {
        flip.consumed = true;
        TT.pageflip.completeCurrentTurn();
      }
    }
  }

  if (TT.navigation.isHomePage()) {
    if (flip.progress > 0.99) {
      $("#front-cover-bookmark").stop(true, true).fadeIn(300);
      $("#front-cover").show();
    } else {
      $("#front-cover").hide();
      if (flip.progress < 0.99) {
        $("#front-cover-bookmark").fadeOut(250, function() {
          $(this).hide();
        });
      }
    }
    if (flip.progress > 0) {
      TT.pageflip.texture = TT.pageflip.textures.front;
      $("#left-page").width(0).hide();
    } else {
      TT.pageflip.texture = TT.pageflip.textures.left;
      if (flip.progress < -0.99) {
        $("#left-page").show().width(TT.BOOK_WIDTH_CLOSED);
      } else {
        $("#left-page").width(0).hide();
        $("#right-page").show();
      }
    }
    $("#page-shadow-overlay").stop(true, true).fadeTo(0.1, flip.progress * 0.3);
  } else {
    if (TT.navigation.isCreditsPage() || TT.navigation.isLastPage()) {
      if (flip.progress < -0.998) {
        if (TT.navigation.isCreditsPage()) {
          $("#back-cover").show();
        } else {
          $("#left-page").show().width(TT.BOOK_WIDTH_CLOSED);
        }
      } else {
        $("#back-cover").hide();
        $("body").addClass("credits");
      }
      if (flip.progress > 0) {
        TT.pageflip.texture = TT.pageflip.textures.right;
        if (flip.progress > 0.996) {
          $("#right-page").show();
          $("body").removeClass("credits");
        } else {
          $("#right-page").hide();
        }
      } else {
        TT.pageflip.texture = TT.pageflip.textures.back;
      }
    } else {
      $("#right-page").show();
      $("#left-page").show().width(TT.BOOK_WIDTH_CLOSED);
    }
  }
  if (flip.target == -1 && flip.progress < -0.95) {
    flip.alpha = 1 - ((Math.abs(flip.progress) - 0.95) / 0.05);
  }
  flip.x = TT.PAGE_WIDTH * flip.progress;
  flip.strength = 1 - (flip.x / TT.PAGE_WIDTH);
  var centralizedFoldStrength = flip.strength > 1 ? 2 - flip.strength : flip.strength;
  if (TT.navigation.isCreditsPage() || TT.navigation.isLastPage()) {
    currentPage.css({
      width: Math.max(flip.x, 0)
    });
  }
  ctx.save();
  ctx.translate(TT.pageflip.CANVAS_HORIZONTAL_PADDING + TT.BOOK_WIDTH_CLOSED, TT.pageflip.CANVAS_VERTICAL_PADDING);
  var scaleX = flip.progress;
  var scaleY = 0;
  var scaleYFactor = 0.35;
  var scaleYFinal = 1 + (1 * scaleYFactor) * centralizedFoldStrength;
  var width = TT.BOOK_WIDTH_CLOSED;
  var height = TT.BOOK_HEIGHT;
  var segments = Math.round(40 + (30 * (0.9999 - ((TT.BOOK_WIDTH_CLOSED * scaleX)) / TT.BOOK_WIDTH_CLOSED)));
  segments = Math.min(width, segments);
  var segmentWidth = width / segments;
  var thickness = 10 * centralizedFoldStrength;
  var hoffset = flip.progress <= 0.05 ? 1 + (1 - (Math.max(flip.progress, 0) / 0.05)) * -thickness : -1;
  var voffset = {
    left: Math.abs(Math.min(flip.progress, 0)) * 2,
    right: flip.progress * 2
  };
  if (Math.abs(scaleX) < 0.99) {
    var ext = ((height - (height * scaleYFinal)) / 2);
    ctx.fillStyle = SERVER_VARIABLES.SOLID_BOOK_COLOR;
    ctx.beginPath();
    ctx.moveTo(0, -0.5);
    ctx.lineTo((width * scaleX) - (2 * scaleX), ext - 0.5);
    ctx.lineTo((width * scaleX) + (thickness + hoffset), ext + voffset.right);
    ctx.lineTo((width * scaleX) + (thickness + hoffset), ext + (height * scaleYFinal) - voffset.right);
    ctx.lineTo((width * scaleX) - (2 * scaleX), ext + (height * scaleYFinal) + 0.5);
    ctx.lineTo(0, height + 0.5);
    ctx.closePath();
    ctx.fill();
  }
  for (var i = 0; i < segments; i++) {
    scaleY = 1 + (i / segments) * scaleYFactor * centralizedFoldStrength;
    var y = (height - (height * scaleY)) / 2;
    var sw = i >= segments - 1 ? segmentWidth : segmentWidth + 3;
    ctx.save();
    ctx.translate(0, y);
    ctx.transform(scaleX, 0, 0, scaleY, 0, 0);
    while ((i * segmentWidth) + sw > TT.BOOK_WIDTH_CLOSED) {
      sw *= 0.9999;
    }
    ctx.drawImage(TT.pageflip.texture, i * segmentWidth, 0, sw, height, i * segmentWidth, 0, sw, height);
    ctx.restore();
  }
  var intensity = Math.max(Math.abs(centralizedFoldStrength), 0.9);
  var ps = {
    top: {
      x: (width * scaleX) + hoffset,
      y: (height - (height * scaleY)) / 2
    },
    bottom: {
      x: (width * scaleX) + hoffset,
      y: ((height - (height * scaleY)) / 2) + height * scaleY
    }
  };
  ctx.fillStyle = SERVER_VARIABLES.SOLID_BOOK_COLOR;
  ctx.beginPath();
  ctx.moveTo(ps.top.x, ps.top.y + voffset.left);
  ctx.lineTo(ps.top.x + thickness, ps.top.y + voffset.right);
  ctx.lineTo(ps.bottom.x + thickness, ps.bottom.y - voffset.right);
  ctx.lineTo(ps.bottom.x, ps.bottom.y - voffset.left);
  ctx.closePath();
  ctx.fill();
  TT.pageflip.dirtyRegion.inflate(TT.PAGE_WIDTH + TT.pageflip.CANVAS_HORIZONTAL_PADDING + TT.PAGE_MARGIN_X - thickness, ps.top.y + TT.pageflip.CANVAS_VERTICAL_PADDING);
  TT.pageflip.dirtyRegion.inflate(TT.PAGE_WIDTH + TT.pageflip.CANVAS_HORIZONTAL_PADDING + (width * scaleX) + thickness, ps.bottom.y + TT.pageflip.CANVAS_VERTICAL_PADDING);
  ctx.restore();
};
TT.pageflip.removeInactiveFlips = function() {
  var activeFlips = 0;
  for (var i = 0; i < TT.pageflip.flips.length; i++) {
    var flip = TT.pageflip.flips[i];
    if (flip.progress === flip.target && (flip.target === 1 || flip.target === -1)) {
      TT.pageflip.flips.splice(i, 1);
      i--;
    } else {
      activeFlips++;
    }
  }
  if (activeFlips == 0) {
    TT.pageflip.deactivate();
  }
};
TT.pageflip.removeHardFlips = function() {
  for (var i = 0; i < TT.pageflip.flips.length; i++) {
    var flip = TT.pageflip.flips[i];
    if (flip.type == TT.pageflip.HARD_FLIP) {
      TT.pageflip.flips.splice(i, 1);
      i--;
    }
  }
};
TT.pageflip.turnToPage = function(currentPage, targetPage, direction, type) {
  if (type == TT.pageflip.HARD_FLIP && !TT.pageflip.dragging) {
    TT.pageflip.removeHardFlips();
  }
  var flip = TT.pageflip.getCurrentFlip();
  if (flip.consumed) {
    flip = TT.pageflip.createFlip();
  }
  TT.pageflip.dragging = false;
  TT.pageflip.turning = true;
  TT.pageflip.hinting = false;
  flip.currentPage = currentPage;
  flip.targetPage = targetPage;
  flip.direction = direction;
  flip.alpha = 1;
  flip.consumed = true;
  flip.type = type || TT.pageflip.SOFT_FLIP;
  flip.target = -1;
  if (direction === -1) {
    flip.target = 1;
    flip.progress = -1;
  }
  if (TT.navigation.isFullScreen()) {
    flip.progress = flip.target * 0.95;
  }
  TT.navigation.updateStatsVisibility(currentPage, false);
  TT.pageflip.activate();
  TT.pageflip.redraw();
};
TT.pageflip.completeCurrentTurn = function() {
  if (TT.pageflip.turning) {
    TT.pageflip.turning = false;
    var flip = TT.pageflip.flips[TT.pageflip.flips.length - 1];
    if (flip) {
      TT.navigation.updateCurrentPointer(flip.currentPage, flip.targetPage);
    }
  }
};
TT.pageflip.getCurrentFlip = function() {
  if (TT.pageflip.flips.length == 0) {
    TT.pageflip.createFlip();
  }
  return TT.pageflip.flips[TT.pageflip.flips.length - 1];
};
TT.pageflip.createFlip = function() {
  if (TT.pageflip.flips.length > 3) {
    TT.pageflip.flips = TT.pageflip.flips.splice(4, 99);
  }
  var flip = new TT.pageflip.Flip();
  TT.pageflip.flips.push(flip);
  return flip;
};
TT.pageflip.getHintRegion = function() {
  var region = new Region();
  if (TT.navigation.isHomePage() || TT.navigation.isLastPage() || TT.navigation.isCreditsPage()) {
    region.left = TT.BOOK_WIDTH_CLOSED - (TT.IS_TOUCH_DEVICE ? TT.pageflip.HINT_WIDTH_TOUCH : TT.pageflip.HINT_WIDTH);
    region.right = TT.BOOK_WIDTH_CLOSED;
  } else {
    region.left = TT.PAGE_WIDTH - (TT.IS_TOUCH_DEVICE ? TT.pageflip.HINT_WIDTH_TOUCH : TT.pageflip.HINT_WIDTH);
    region.right = TT.PAGE_WIDTH;
  }
  region.top = 0;
  region.bottom = TT.PAGE_HEIGHT;
  return region;
};
TT.pageflip.isMouseInHintRegion = function() {
  return TT.pageflip.getHintRegion().contains(TT.pageflip.mouse.x, TT.pageflip.mouse.y);
};
TT.pageflip.onKeyPress = function(event) {
  if (!TT.search.hasFocus) {
    var hasPassedLockdown = TT.time() - TT.pageflip.lastKeyboardNavigationTime > 1000;
    if (event.keyCode == 37 && (TT.pageflip.lastKeyboardNavigationDirection === -1 || hasPassedLockdown)) {
      TT.navigation.goToPreviousPage();
      TT.pageflip.lastKeyboardNavigationDirection = -1;
      TT.pageflip.lastKeyboardNavigationTime = TT.time();
      event.preventDefault();
      return false;
    } else {
      if (event.keyCode == 39 && (TT.pageflip.lastKeyboardNavigationDirection === 1 || hasPassedLockdown)) {
        TT.navigation.goToNextPage();
        TT.pageflip.lastKeyboardNavigationDirection = 1;
        TT.pageflip.lastKeyboardNavigationTime = TT.time();
        event.preventDefault();
        return false;
      } else {
        if (event.keyCode == 27) {
          TT.fullscreen.exit();
          event.preventDefault();
          return false;
        }
      }
    }
  }
};
TT.pageflip.handlePointerDown = function() {
  if (TT.pageflip.isMouseInHintRegion()) {
    $("body").css("cursor", "pointer");
    if (TT.time() - TT.pageflip.mouseDownTime > TT.pageflip.CLICK_FREQUENCY) {
      TT.pageflip.dragging = true;
    }
    TT.pageflip.mouseDownTime = TT.time();
    TT.pageflip.activate();
  }
};
TT.pageflip.handlePointerMove = function() {
  var hinting = TT.pageflip.hinting;
  TT.pageflip.hinting = false;
  $("body").css("cursor", "");
  if (!TT.pageflip.dragging && !TT.pageflip.turning && (!TT.navigation.isCreditsPage() || (TT.navigation.isCreditsPage() && TT.navigation.isBookOpen()))) {
    var flip = TT.pageflip.getCurrentFlip();
    if (flip.progress < 0) {
      flip = TT.pageflip.createFlip();
    }
    var isHardCover = (TT.navigation.isHomePage() || TT.navigation.isLastPage() || (TT.navigation.isCreditsPage() && TT.navigation.isBookOpen()));

    flip.type = isHardCover ? TT.pageflip.HARD_FLIP : TT.pageflip.SOFT_FLIP;
    if (TT.pageflip.isMouseInHintRegion()) {
      if (TT.pageflip.mouseHistory[4]) {
        var distanceX = TT.pageflip.mouse.x - (TT.pageflip.mouseHistory[4].x || 0);
        var distanceY = TT.pageflip.mouse.y - (TT.pageflip.mouseHistory[4].y || 0);
        var distanceTravelled = Math.sqrt(distanceX * distanceX + distanceY * distanceY);
      } else {
        var distanceTravelled = 0;
      }
      if (!TT.navigation.isHomePage() || distanceTravelled < 100) {
        flip.target = Math.min(TT.pageflip.mouse.x / TT.PAGE_WIDTH, 0.98);
        $("body").css("cursor", "pointer");
        TT.pageflip.activate();
        TT.pageflip.hinting = true;
        if (TT.navigation.isHomePage()) {
          flip.target = Math.min(TT.pageflip.mouse.x / TT.PAGE_WIDTH, 0.95);
          $("#pages section.current").show().width(TT.PAGE_WIDTH);
        } else {
          $("#pages section.current").next("section").show().width(TT.PAGE_WIDTH);
        }
      }
    } else {
      if (flip.progress !== 1 && flip.target !== -1) {
        if (TT.pageflip.hinting == true) {
          $("#pages section.current").next("section").width(0);
        }
        flip.target = 1;
        TT.pageflip.activate();
        TT.pageflip.hinting = false;
      }
    }
  } else {
    if (TT.pageflip.dragging) {
      if (TT.pageflip.getCurrentFlip().type != TT.pageflip.HARD_FLIP) {
        TT.pageflip.getCurrentFlip().alpha = 1;
      }
    }
  }
  while (TT.pageflip.mouseHistory.length > 9) {
    TT.pageflip.mouseHistory.pop();
  }
  TT.pageflip.mouseHistory.unshift(TT.pageflip.mouse);
};
TT.pageflip.handlePointerUp = function() {
  if (TT.time() - TT.pageflip.mouseDownTime < TT.pageflip.CLICK_FREQUENCY) {
    TT.navigation.goToNextPage();
    TT.pageflip.dragging = false;
    return false;
  }
  if (TT.pageflip.dragging && TT.pageflip.mouse.x < TT.PAGE_WIDTH * 0.45) {
    var succeeded = TT.navigation.goToNextPage();
    if (succeeded == false) {
      TT.pageflip.dragging = false;
    }
  } else {
    TT.pageflip.dragging = false;
    TT.pageflip.handlePointerMove();
  }
};
TT.pageflip.onMouseDown = function(event) {
  TT.pageflip.mouse.down = true;
  TT.pageflip.updateRelativeMousePosition(event.clientX, event.clientY);
  TT.pageflip.handlePointerDown();
  if (TT.pageflip.isMouseInHintRegion()) {
    event.preventDefault();
    return false;
  }
};
TT.pageflip.onMouseMove = function(event) {
  TT.pageflip.updateRelativeMousePosition(event.clientX, event.clientY);
  TT.pageflip.handlePointerMove();
};
TT.pageflip.onMouseUp = function(event) {
  TT.pageflip.mouse.down = false;
  TT.pageflip.updateRelativeMousePosition(event.clientX, event.clientY);
  TT.pageflip.handlePointerUp();
};
TT.pageflip.onTouchStart = function(event) {
  if (event.touches.length == 1) {
    var globalX = event.touches[0].pageX - (window.innerWidth - TT.PAGE_WIDTH) * 0.5;
    var globalY = event.touches[0].pageY - (window.innerHeight - TT.PAGE_HEIGHT) * 0.5;
    TT.pageflip.updateRelativeMousePosition(globalX, globalY);
    TT.pageflip.mouse.down = true;
    if (TT.pageflip.isMouseInHintRegion()) {
      event.preventDefault();
      TT.pageflip.handlePointerDown();
    }
  }
};
TT.pageflip.onTouchMove = function(event) {
  if (event.touches.length == 1) {
    var globalX = event.touches[0].pageX - (window.innerWidth - TT.PAGE_WIDTH) * 0.5;
    var globalY = event.touches[0].pageY - (window.innerHeight - TT.PAGE_HEIGHT) * 0.5;
    TT.pageflip.updateRelativeMousePosition(globalX, globalY);
    if (TT.pageflip.isMouseInHintRegion()) {
      event.preventDefault();
      TT.pageflip.handlePointerMove();
    }
  }
};
TT.pageflip.onTouchEnd = function(event) {
  TT.pageflip.mouse.down = false;
  TT.pageflip.handlePointerUp();
};
TT.pageflip.getRelativeMousePosition = function(globalX, globalY) {
  var point = {
    x: globalX,
    y: globalY
  };
  point.x -= $("#pages").offset().left + TT.PAGE_WIDTH;
  point.y -= $("#pages").offset().top;
  return point;
};
TT.pageflip.updateRelativeMousePosition = function(globalX, globalY) {
  var point = TT.pageflip.getRelativeMousePosition(globalX, globalY);
  TT.pageflip.mouse.x = point.x;
  TT.pageflip.mouse.y = point.y;
};
TT.pageflip.Flip = function() {
  this.id = Math.round(Math.random() * 1000);
  this.currentPage = $("#pages section.current");
  this.targetPage = $("#pages section.current");
  this.direction = -1;
  this.progress = 1;
  this.target = 1;
  this.strength = 0;
  this.alpha = 1;
  this.type = TT.pageflip.SOFT_FLIP;
  this.x = 0;
  this.consumed = false;
};

function Region() {
  this.left = 999999;
  this.top = 999999;
  this.right = 0;
  this.bottom = 0;
}
Region.prototype.reset = function() {
  this.left = 999999;
  this.top = 999999;
  this.right = 0;
  this.bottom = 0;
};
Region.prototype.inflate = function(x, y) {
  this.left = Math.min(this.left, x);
  this.top = Math.min(this.top, y);
  this.right = Math.max(this.right, x);
  this.bottom = Math.max(this.bottom, y);
};
Region.prototype.contains = function(x, y) {
  return x > this.left && x < this.right && y > this.top && y < this.bottom;
};
Region.prototype.toRectangle = function(padding) {
  padding |= 0;
  return {
    x: this.left - padding,
    y: this.top - padding,
    width: this.right - this.left + (padding * 2),
    height: this.bottom - this.top + (padding * 2)
  };
};
TT.paperstack = {};
TT.paperstack.container = null;
TT.paperstack.initialize = function() {
  TT.paperstack.container = $("#paperstack");
};
TT.paperstack.updateStack = function(overrideProgress) {
  // var availablePapers = $("#pages section").length;
  var availablePapers = $("div.paper", TT.paperstack.container).length;
  // var visiblePapers = Math.round(((1 - (overrideProgress ? overrideProgress : TT.chapternav.getProgress())) * availablePapers));
  var visiblePapers = availablePapers - TT.chapternav.getProgress();

  if (visiblePapers != 0) {
    $(".paper:lt(" + visiblePapers + ")", TT.paperstack.container).css({
      opacity: 1
    });
    $(".paper:gt(" + visiblePapers + ")", TT.paperstack.container).css({
      opacity: 0
    });
    $(".shadow", TT.paperstack.container).css({
      opacity: 1
    });
  } else {
    $(".paper", TT.paperstack.container).css({
      opacity: 0
    });
    $(".shadow", TT.paperstack.container).css({
      opacity: 0
    });
  }
  $(".shadow", TT.paperstack.container).css({
    marginLeft: visiblePapers-availablePapers-4
  });
};
TT.illustrations = {};
TT.illustrations.FRAME_RATE = 30;
TT.illustrations.ASSETS_URL = "/media/illustrations/";
TT.illustrations.interval = -1;
TT.illustrations.update = function(currentPage) {
  TT.illustrations.deactivate();
  if (currentPage && !TT.navigation.isHomePage() && !TT.navigation.isFullScreen()) {
    TT.log("Activate animation: " + currentPage.attr("class"));
    if (currentPage.hasClass("title-html") && currentPage.hasClass("page-3")) {
      TT.illustrations.html.activate($("div.image1", currentPage));
    } else {
      if (currentPage.hasClass("title-foreword") && currentPage.hasClass("page-1")) {
        TT.illustrations.cloud.activate($("div.image1", currentPage));
      } else {
        if (currentPage.hasClass("title-open-source") && currentPage.hasClass("page-1")) {
          TT.illustrations.opensource.activate($("div.image1", currentPage));
        } else {
          if (currentPage.hasClass("title-what-is-the-internet") && currentPage.hasClass("page-1")) {
            TT.illustrations.internet.activate($("div.image1", currentPage));
          } else {
            if (currentPage.hasClass("title-page-load") && currentPage.hasClass("page-1")) {
              TT.illustrations.pageload.activate($("div.image1", currentPage));
            } else {
              if (currentPage.hasClass("title-web-apps") && currentPage.hasClass("page-1")) {
                TT.illustrations.webapps.activate($("div.image1", currentPage));
              } else {
                if (currentPage.hasClass("title-threed") && currentPage.hasClass("page-1")) {
                  TT.illustrations.threed.activate($("div.image1", currentPage));
                }
              }
            }
          }
        }
      }
    }
  }
};
TT.illustrations.deactivate = function() {
  clearInterval(TT.illustrations.interval);
};
TT.illustrations.createCanvas = function(parent, world) {
  var canvas = $("<canvas></canvas>");
  canvas[0].width = world.width;
  canvas[0].height = world.height;
  parent.append(canvas);
  TT.illustrations.updateCanvasPosition(parent, world);
  return canvas;
};
TT.illustrations.updateCanvasPosition = function(parent, world) {
  var canvas = $("canvas", parent);
  canvas.css({
    position: "absolute",
    left: $("img", parent).position().left + world.x,
    top: $("img", parent).position().top + world.y
  });
  return $("img", parent).width() !== 0 || $("img", parent).height() !== 0;
};
TT.illustrations.threed = {
  canvas: null,
  context: null,
  container: null,
  image: null,
  cloudImage: null,
  clouds: [],
  alpha: 0,
  world: {
    x: 0,
    y: 0,
    width: 320,
    height: 150
  },
  positioned: false,
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
      this.cloudImage = new Image();
      this.cloudImage.src = TT.illustrations.ASSETS_URL + "3d01_clouds.png";
      this.clouds.push({
        source: {
          x: 0,
          y: 0,
          width: 63,
          height: 35
        },
        x: 44,
        y: 16,
        originalX: 44,
        originalY: 16,
        velocity: {
          x: 0,
          y: 0
        }
      });
      this.clouds.push({
        source: {
          x: 0,
          y: 36,
          width: 70,
          height: 40
        },
        x: 147,
        y: 10,
        originalX: 147,
        originalY: 10,
        velocity: {
          x: 0,
          y: 0
        }
      });
      this.clouds.push({
        source: {
          x: 0,
          y: 78,
          width: 84,
          height: 50
        },
        x: 213,
        y: 48,
        originalX: 212,
        originalY: 48,
        velocity: {
          x: 0,
          y: 0
        }
      });
    } else {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.threed.draw();
  },
  draw: function() {
    if (!this.positioned) {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    if (this.cloudImage.complete) {
      this.alpha = Math.min(this.alpha + 0.1, 1);
      this.context.globalAlpha = this.alpha;
      for (var i = 0; i < this.clouds.length; i++) {
        var cloud = this.clouds[i];
        cloud.x += cloud.velocity.x;
        cloud.y += cloud.velocity.y;
        cloud.velocity.x *= 0.96;
        cloud.velocity.y *= 0.96;
        var speed = 0.3;
        if (Math.abs(cloud.velocity.x) < 0.01) {
          if (cloud.x > cloud.originalX) {
            cloud.velocity.x -= 0.05 + Math.random() * speed;
          } else {
            cloud.velocity.x += 0.05 + Math.random() * speed;
          }
        }
        if (Math.abs(cloud.velocity.y) < 0.01) {
          if (cloud.y > cloud.originalY) {
            cloud.velocity.y -= 0.01 + Math.random() * speed;
          } else {
            cloud.velocity.y += 0.01 + Math.random() * speed;
          }
        }
        this.context.save();
        this.context.translate(cloud.x, cloud.y);
        this.context.drawImage(this.cloudImage, cloud.source.x, cloud.source.y, cloud.source.width, cloud.source.height, 0, 0, cloud.source.width, cloud.source.height);
        this.context.restore();
      }
    }
  }
};
TT.illustrations.webapps = {
  GRAVITY: 0.04,
  canvas: null,
  context: null,
  container: null,
  image: null,
  leaves: [],
  points: [{
    x: 86,
    y: 100
  }, {
    x: 35,
    y: 88
  }, {
    x: 168,
    y: 35
  }, {
    x: 250,
    y: 15
  }],
  world: {
    x: 20,
    y: 30,
    width: 300,
    height: 260
  },
  positioned: false,
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
    } else {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.webapps.draw();
  },
  draw: function() {
    if (!this.positioned) {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    if (this.leaves.length < 4 && Math.random() > 0.9) {
      var point = this.points[Math.floor(Math.random() * this.points.length)];
      this.leaves.push({
        x: point.x,
        y: point.y,
        w: 18 + (Math.random() * 8),
        h: 6 + (Math.random() * 4),
        alpha: 0,
        rotation: Math.random() * Math.PI,
        velocity: {
          x: -0.2 + (Math.random() * 0.4),
          y: Math.random() * 2,
          rotation: -0.1 + (Math.random() * 0.2)
        }
      });
    }
    for (var i = 0; i < this.leaves.length; i++) {
      var leaf = this.leaves[i];
      leaf.velocity.y += this.GRAVITY;
      if (leaf.y > this.world.height + 20) {
        this.leaves.splice(i, 1);
        i--;
        continue;
      }
      leaf.x += leaf.velocity.x;
      leaf.y += leaf.velocity.y;
      leaf.rotation += leaf.velocity.rotation;
      leaf.alpha = Math.min(leaf.alpha + 0.1, 1);
      this.context.save();
      var b = 3;
      this.context.globalAlpha = leaf.alpha;
      this.context.beginPath();
      this.context.translate(leaf.x, leaf.y);
      this.context.rotate(leaf.rotation);
      this.context.strokeStyle = "rgba(0,100,20,0.7)";
      this.context.fillStyle = "rgba(159,192,94,0.9)";
      this.context.moveTo(0, leaf.h / 2);
      this.context.quadraticCurveTo(leaf.w / 2, -b, leaf.w, leaf.h / 2);
      this.context.quadraticCurveTo(leaf.w / 2, leaf.h + b, 0, leaf.h / 2);
      this.context.stroke();
      this.context.fill();
      this.context.restore();
    }
    var mask = this.context.createLinearGradient(0, 0, 0, this.world.height);
    mask.addColorStop(0.7, "rgba(255, 255, 255, 0)");
    mask.addColorStop(1, "rgba(255, 255, 255, 1)");
    this.context.save();
    this.context.globalCompositeOperation = "destination-out";
    this.context.beginPath();
    this.context.fillStyle = mask;
    this.context.fillRect(0, 0, this.world.width, this.world.height);
    this.context.restore();
  }
};
TT.illustrations.pageload = {
  GRAVITY: 0.04,
  canvas: null,
  context: null,
  container: null,
  image: null,
  bubbles: [],
  world: {
    x: 10,
    y: 100,
    width: 220,
    height: 100
  },
  positioned: false,
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
    } else {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.pageload.draw();
  },
  draw: function() {
    if (!this.positioned) {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    if (this.bubbles.length < 7 && Math.random() > 0.85) {
      this.bubbles.push({
        x: Math.random() * this.world.width,
        y: this.world.height + 10,
        alpha: 0,
        size: 1 + Math.random() * 3,
        velocity: {
          x: -0.4 + (Math.random() * 0.8),
          y: Math.random() * -2
        }
      });
    }
    for (var i = 0; i < this.bubbles.length; i++) {
      var bubble = this.bubbles[i];
      bubble.velocity.y -= this.GRAVITY;
      if (bubble.y < -10) {
        this.bubbles.splice(i, 1);
        i--;
        continue;
      } else {
        if (bubble.y < this.world.height * 0.3) {
          bubble.alpha = Math.max(bubble.y / (this.world.height * 0.3), 0);
        } else {
          if (bubble.y > this.world.height * 0.7) {
            bubble.alpha = 1 - Math.min((bubble.y - this.world.height * 0.7) / (this.world.height * 0.3), 1);
          }
        }
      }
      bubble.x += bubble.velocity.x;
      bubble.y += bubble.velocity.y;
      this.context.beginPath();
      this.context.strokeStyle = "rgba( 0, 0, 0, " + (bubble.alpha * 0.3) + " )";
      this.context.fillStyle = "rgba( 0, 180, 250, " + (bubble.alpha * 0.7) + " )";
      this.context.arc(bubble.x, bubble.y, bubble.size, 0, Math.PI * 2, true);
      this.context.stroke();
    }
    var mask = this.context.createLinearGradient(0, 0, -25, this.world.height);
    mask.addColorStop(0, "rgba(255, 255, 255, 1)");
    mask.addColorStop(0.6, "rgba(255, 255, 255, 0)");
    this.context.save();
    this.context.globalCompositeOperation = "destination-out";
    this.context.beginPath();
    this.context.fillStyle = mask;
    this.context.fillRect(0, 0, this.world.width, this.world.height);
    this.context.restore();
  }
};
TT.illustrations.internet = {
  GRAVITY: 0.04,
  canvas: null,
  context: null,
  container: null,
  image: null,
  zero: null,
  one: null,
  numbers: [],
  positioned: false,
  world: {
    x: 345,
    y: 115,
    width: 120,
    height: 80
  },
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
      this.zero = new Image();
      this.zero.src = TT.illustrations.ASSETS_URL + "internet01-part1.png";
      this.one = new Image();
      this.one.src = TT.illustrations.ASSETS_URL + "internet01-part2.png";
    } else {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.internet.draw();
  },
  draw: function() {
    if (!this.positioned) {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    if (this.zero.complete && this.one.complete) {
      if (this.numbers.length < 20 && Math.random() > 0.6) {
        this.numbers.push({
          type: Math.random() > 0.5 ? 1 : 0,
          x: 5,
          y: 0,
          alpha: 0,
          rotation: Math.random() * Math.PI,
          velocity: {
            x: 0.4 + (Math.random() * 1.6),
            y: Math.random() * 2,
            rotation: -0.1 + (Math.random() * 0.2)
          }
        });
      }
      for (var i = 0; i < this.numbers.length; i++) {
        var number = this.numbers[i];
        var image = number.type == 0 ? this.zero : this.one;
        number.velocity.y += this.GRAVITY;
        if (number.y > this.world.height + image.height) {
          this.numbers.splice(i, 1);
          i--;
          continue;
        } else {} if (number.y < this.world.height * 0.1) {
          number.alpha = Math.min(number.y / (this.world.height * 0.1), 1);
        } else {} if (number.y > this.world.height * 0.6) {
          number.alpha = 1 - Math.min((number.y - this.world.height * 0.5) / (this.world.height * 0.3), 1);
        }
        number.x += number.velocity.x;
        number.y += number.velocity.y;
        number.rotation += number.velocity.rotation;
        this.context.save();
        this.context.globalAlpha = number.alpha;
        this.context.translate(number.x + Math.round(image.width * 0.5), number.y + Math.round(image.height * 0.5));
        this.context.rotate(number.rotation);
        this.context.translate(-Math.round(image.width * 0.5), -Math.round(image.height * 0.5));
        this.context.drawImage(image, 0, 0);
        this.context.restore();
      }
    }
  }
};
TT.illustrations.opensource = {
  canvas: null,
  context: null,
  container: null,
  image: null,
  cog1: {
    image: null,
    x: 57,
    y: 14,
    currentRotation: 0,
    targetRotation: 0,
    lastUpdate: 0
  },
  cog2: {
    image: null,
    x: 28,
    y: 38,
    currentRotation: 0,
    targetRotation: 0,
    lastUpdate: 0
  },
  alpha: 0,
  world: {
    x: 90,
    y: 37,
    width: 100,
    height: 100
  },
  positioned: false,
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
      this.cog1.image = new Image();
      this.cog1.image.src = TT.illustrations.ASSETS_URL + "opensource01-part1.png";
      this.cog2.image = new Image();
      this.cog2.image.src = TT.illustrations.ASSETS_URL + "opensource01-part2.png";
    } else {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    this.cog1.lastUpdate = TT.time();
    this.cog2.lastUpdate = TT.time();
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.opensource.draw();
  },
  draw: function() {
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    if (!this.positioned) {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
    if (this.cog1.image.complete && this.cog2.image.complete) {
      this.alpha = Math.min(this.alpha + 0.08, 1);
      if (this.cog1.currentRotation > this.cog1.targetRotation - 1 && TT.time() - this.cog1.lastUpdate > 2000) {
        this.cog1.targetRotation += Math.PI / 3;
        this.cog1.lastUpdate = TT.time();
      }
      if (this.cog2.currentRotation > this.cog2.targetRotation - 1 && TT.time() - this.cog2.lastUpdate > 6000) {
        this.cog2.targetRotation += Math.PI / 9;
        this.cog2.lastUpdate = TT.time();
      }
      this.cog1.currentRotation += (this.cog1.targetRotation - this.cog1.currentRotation) * 0.5;
      this.cog2.currentRotation += (this.cog2.targetRotation - this.cog2.currentRotation) * 0.4;
      if (Math.abs(this.cog1.currentRotation - this.cog1.targetRotation) < 0.05) {
        this.cog1.currentRotation = this.cog1.targetRotation;
      }
      if (Math.abs(this.cog2.currentRotation - this.cog2.targetRotation) < 0.05) {
        this.cog2.currentRotation = this.cog2.targetRotation;
      }
      this.context.save();
      this.context.globalAlpha = this.alpha;
      this.context.save();
      this.context.translate(this.cog1.x + Math.round(this.cog1.image.width * 0.5), this.cog1.y + Math.round(this.cog1.image.height * 0.5));
      this.context.rotate(this.cog1.currentRotation);
      this.context.translate(-Math.round(this.cog1.image.width * 0.5), -Math.round(this.cog1.image.height * 0.5));
      this.context.drawImage(this.cog1.image, 0, 0);
      this.context.restore();
      this.context.save();
      this.context.translate(this.cog2.x + Math.round(this.cog2.image.width * 0.5), this.cog2.y + Math.round(this.cog2.image.height * 0.5));
      this.context.rotate(this.cog2.currentRotation);
      this.context.translate(-Math.round(this.cog2.image.width * 0.5), -Math.round(this.cog2.image.height * 0.5));
      this.context.drawImage(this.cog2.image, 0, 0);
      this.context.restore();
      this.context.restore();
    }
  }
};
TT.illustrations.cloud = {
  canvas: null,
  context: null,
  container: null,
  image: null,
  cloutImage: null,
  world: {
    x: 0,
    y: 0,
    width: 240,
    height: 200
  },
  positioned: false,
  clouds: [{
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }, {
    x: Math.random() * 240,
    y: Math.random() * 200,
    strength: 1,
    velocity: {
      x: 0,
      y: 0
    },
    size: 8 + Math.random() * 8
  }],
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
      this.cloudImage = new Image();
      this.cloudImage.src = TT.illustrations.ASSETS_URL + "3d01_clouds.png";
    } else {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.cloud.draw();
  },
  draw: function() {
    if (!this.positioned) {
      this.positioned = TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    if (this.image[0].complete) {
      this.context.drawImage(this.image[0], 0, 0);
    }
    var speed = 3;
    for (var i = 0, len = this.clouds.length; i < len; i++) {
      var cloud = this.clouds[i];
      cloud.velocity.x /= 1.04;
      cloud.velocity.y /= 1.04;
      if (Math.abs(cloud.velocity.x) < 0.2) {
        if (cloud.x > this.world.width / 2) {
          cloud.velocity.x -= 0.7 + Math.random() * speed;
        } else {
          cloud.velocity.x += 0.7 + Math.random() * speed;
        }
      }
      if (Math.abs(cloud.velocity.y) < 0.2) {
        if (cloud.y > this.world.height / 2) {
          cloud.velocity.y -= 0.5 + Math.random() * speed;
        } else {
          cloud.velocity.y += 0.5 + Math.random() * speed;
        }
      }
      cloud.x += cloud.velocity.x;
      cloud.y += cloud.velocity.y;
      cloud.strength = Math.max(Math.min(cloud.strength, 1), 0);
      var gradient = this.context.createRadialGradient(cloud.x, cloud.y, 0, cloud.x, cloud.y, cloud.size);
      this.context.save();
      var browser = BrowserDetect.browser.toLowerCase();
      if (browser == "firefox") {
        gradient.addColorStop(0.4, "rgba(255,255,255," + (cloud.strength * 0.7) + ")");
        gradient.addColorStop(1, "rgba(255,255,255,0)");
      } else {
        gradient.addColorStop(0.4, "rgba(90,170,190," + (cloud.strength) + ")");
        gradient.addColorStop(1, "rgba(90,170,190,0)");
        this.context.globalCompositeOperation = "source-in";
      }
      this.context.beginPath();
      this.context.fillStyle = gradient;
      this.context.arc(cloud.x, cloud.y, cloud.size, 0, Math.PI * 2, true);
      this.context.fill();
      this.context.restore();
    }
  }
};
TT.illustrations.html = {
  canvas: null,
  context: null,
  container: null,
  image: null,
  world: {
    x: 100,
    y: -15,
    width: 150,
    height: 200
  },
  bulbs: [{
    x: 27,
    y: 22,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 62,
    y: 30,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 90,
    y: 39,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 117,
    y: 48,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 22,
    y: 59,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 23,
    y: 89,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 24,
    y: 115,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 25,
    y: 139,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 124,
    y: 87,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 124,
    y: 116,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 124,
    y: 144,
    strength: 0,
    momentum: 0,
    size: 10
  }, {
    x: 124,
    y: 178,
    strength: 0,
    momentum: 0,
    size: 10
  }],
  initialize: function(container) {
    if (this.canvas === null) {
      this.container = container;
      this.image = $("img", container);
      this.canvas = TT.illustrations.createCanvas(container, this.world);
      this.context = this.canvas[0].getContext("2d");
    } else {
      TT.illustrations.updateCanvasPosition(this.container, this.world);
    }
  },
  activate: function(container) {
    this.initialize(container);
    TT.illustrations.interval = setInterval(this.render, 1000 / TT.illustrations.FRAME_RATE);
  },
  render: function() {
    TT.illustrations.html.draw();
  },
  draw: function() {
    this.context.clearRect(0, 0, this.world.width, this.world.height);
    for (var i = 0, len = this.bulbs.length; i < len; i++) {
      var bulb = this.bulbs[i];
      if (bulb.strength < 0.1 && bulb.momentum <= 0 && Math.random() > 0.98) {
        bulb.momentum = Math.random() * 0.3;
      } else {
        if (bulb.strength >= 1 && Math.random() > 0.98) {
          bulb.momentum = -Math.random() * 0.3;
        }
      }
      bulb.strength += bulb.momentum;
      bulb.strength = Math.max(Math.min(bulb.strength, 1), 0);
      var gradient = this.context.createRadialGradient(bulb.x, bulb.y, 0, bulb.x, bulb.y, bulb.size);
      gradient.addColorStop(0.4, "rgba(255,255,100," + (bulb.strength * 0.95) + ")");
      gradient.addColorStop(1, "rgba(255,255,100,0)");
      this.context.beginPath();
      this.context.fillStyle = gradient;
      this.context.arc(bulb.x, bulb.y, bulb.size, 0, Math.PI * 2, true);
      this.context.fill();
    }
  }
};
TT.navigation = {};
TT.navigation.transitioningFromHardCover = false;
TT.navigation.hasNavigated = false;
TT.navigation.currentPageName = "";
TT.navigation.currentThing = "";
TT.navigation.enqueueNavigation = null;
TT.navigation.initialize = function() {
  $("#pages section:not(.current)").width(0).hide();
  TT.navigation.assignNavigationHandlers();
  TT.navigation.assignNextPrevHandlers();
  if (TT.navigation.isHomePage()) {
    TT.flipintro.activate();
  } else {
    $("#front-cover").hide();
    $("#front-cover-bookmark").hide();
    $("#front-cover-arrow").hide();
  }
  if (!TT.navigation.isCreditsPage()) {
    $("#back-cover").hide();
  }
  if (TT.navigation.isTableOfThings()) {
    $("body").addClass("home").addClass("tot");
  } else {
    if (!TT.navigation.isHomePage() && !TT.navigation.isCreditsPage()) {
      $("body").addClass("book");
    }
  }
  TT.sharing.updateSharer();
  TT.navigation.loadImages();
  TT.illustrations.update($("#pages section.current"));
  TT.navigation.updatePageVisibility($("#pages section.current"));
  TT.navigation.updateStatsVisibility($("#pages section.current"), true);
};
TT.navigation.assignNavigationHandlers = function() {
  $("header a.logo").click(function() {
    TT.navigation.goToHome();
    return false;
  });
  $("header li.about a").click(function() {
    TT.navigation.goToPage(TT.history.FOREWORD, 1);
    return false;
  });
  $("header li.credits a").click(function() {
    TT.navigation.goToCredits();
    return false;
  });
  $("#front-cover-bookmark a.open-book").click(function() {
    TT.navigation.goToNextPage();
    return false;
  });
  $("header li.table-of-things a").click(function() {
    TT.tableofthings.show();
    return false;
  });
  $("#table-of-contents a.go-back").click(function() {
    TT.tableofthings.hide();
    return false;
  });
  $("#front-cover-arrow").click(function() {
    TT.navigation.goToNextPage();
    return false;
  });
  $("footer .print a").click(function() {
    if (window.location.pathname.match("en-US")) {
      TT.overlay.showPrint();
      return false;
    }
  });
  $("#pages section a").click(function() {
    var link = $(this).attr("href");
    if (link.indexOf("http://") == -1 && link.indexOf("www.") == -1) {
      var article = link.split("/")[1];
      var page = link.split("/")[2];
      if (article && page) {
        TT.navigation.goToPage(article, page);
      }
      return false;
    }
  });
};
TT.navigation.assignNextPrevHandlers = function() {
  $("#pagination-prev").click(function(e) {
    e.preventDefault();
    TT.navigation.goToPreviousPage();
  });
  $("#pagination-next").click(function(e) {
    e.preventDefault();
    TT.navigation.goToNextPage();
  });
  var element = '<div class="page-progress"><p class="thing"></p><p class="number">' + SERVER_VARIABLES.PAGE + " <span></span></p></div>";
  if (!TT.IS_TOUCH_DEVICE) {
    $("#pagination-prev").append(element);
    $("#pagination-next").append(element);
  }
};
TT.navigation.isHomePage = function() {
  return $("body").hasClass("home");
};
TT.navigation.isCreditsPage = function() {
  return $("body").hasClass("credits");
};
TT.navigation.isTableOfThings = function() {
  return $("body").hasClass("tot");
};
TT.navigation.isBookOpen = function() {
  return $("body").hasClass("book");
};
TT.navigation.isFullScreen = function() {
  return $("body").hasClass("fullscreen");
};
TT.navigation.isForeword = function(target) {
  if (!target) {
    target = $("#pages section.current");
  }
  return TT.navigation.classToArticle(target.attr("class")) == TT.history.FOREWORD;
};
TT.navigation.isLastPage = function(target) {
  if (target) {
    return target.next("section").length == 0 && !TT.navigation.isCreditsPage();
  }
  return $("#pages section.current").next("section").length == 0 && !TT.navigation.isCreditsPage();
};
TT.navigation.isFirstPage = function(target) {
  if (target) {
    return target.prev("section").length == 0 && !TT.navigation.isHomePage();
  }
  return $("#pages section.current").prev("section").length == 0 && !TT.navigation.isHomePage();
};
TT.navigation.classToArticle = function(theClass) {
  return theClass ? theClass.match(/title-([a-zA-Z-0-9]+)/)[1] : null;
};
TT.navigation.classToArticlePage = function(theClass) {
  return theClass ? parseInt(theClass.match(/page-([0-9]+)/)[1]) : null;
};
TT.navigation.classToGlobalPage = function(theClass) {
  return theClass ? parseInt(theClass.match(/globalPage-([0-9]+)/)[1]) : null;
};
TT.navigation.updateNextPrevLinks = function(targetPage) {
  if (TT.navigation.isCreditsPage()) {
    $("#pagination-next").addClass("inactive");
    $("#pagination-prev").removeClass("inactive");
  } else {
    if (TT.navigation.isHomePage()) {
      $("#pagination-prev").addClass("inactive");
      $("#pagination-next").removeClass("inactive");
    } else {
      $("#pagination-prev, #pagination-next").removeClass("inactive");
    }
  }
  var nextPage = TT.navigation.isHomePage() ? targetPage.attr("class") : targetPage.next("section").attr("class");
  var prevPage = targetPage.prev("section").attr("class");
  if (nextPage) {
    TT.navigation.updatePaginationHint(nextPage, $("#pagination-next"));
  } else {
    $("#pagination-next .page-progress").hide();
  }
  if (prevPage && !TT.navigation.isLastPage() && !TT.navigation.isCreditsPage()) {
    TT.navigation.updatePaginationHint(prevPage, $("#pagination-prev"));
  } else {
    $("#pagination-prev .page-progress").hide();
  }
};
TT.navigation.updatePaginationHint = function(page, button) {
  var articleId = TT.navigation.classToArticle(page);
  var articleIndex = $("#chapter-nav ul li").find("[data-article=" + articleId + "]").parent().index() + 1;
  var pageNumber = TT.navigation.classToArticlePage(page);
  var numberOfPages = $("#pages section.title-" + articleId).length;
  if (pageNumber != undefined && numberOfPages != undefined) {
    $(".page-progress", button).show();
    if (articleId == TT.history.FOREWORD) {
      $("p.thing", button).html(SERVER_VARIABLES.FOREWORD);
    } else {
      $("p.thing", button).html(SERVER_VARIABLES.THING + " " + articleIndex);
    }
    $("p.number span", button).text(pageNumber + "/" + numberOfPages);
  } else {
    $(".page-progress", button).hide();
  }
};
TT.navigation.getCurrentArticleId = function() {
  return TT.navigation.classToArticle($("#pages section.current").attr("class"));
};
TT.navigation.getCurrentArticlePage = function() {
  return TT.navigation.classToArticlePage($("#pages section.current").attr("class"));
};
TT.navigation.goToPreviousPage = function() {
  TT.navigation.cleanUpTransitions();
  if (TT.navigation.transitioningFromHardCover) {
    return false;
  }
  if (TT.navigation.isFirstPage()) {
    if (!TT.navigation.isHomePage()) {
      TT.pageflip.completeCurrentTurn();
      TT.navigation.goToHome();
    }
    return false;
  }
  TT.pageflip.completeCurrentTurn();
  var currentPage = $("#pages section.current");
  var prevArticle, prevPage = null;
  if (TT.navigation.isCreditsPage()) {
    prevArticle = TT.navigation.classToArticle(currentPage.attr("class"));
    prevPage = TT.navigation.classToArticlePage(currentPage.attr("class"));
  } else {
    prevArticle = TT.navigation.classToArticle(currentPage.prev("section").attr("class"));
    prevPage = TT.navigation.classToArticlePage(currentPage.prev("section").attr("class"));
  }
  TT.navigation.goToPage(prevArticle, prevPage);
};
TT.navigation.goToNextPage = function() {
  TT.navigation.cleanUpTransitions();
  if (TT.navigation.transitioningFromHardCover) {
    return false;
  }
  if (TT.navigation.isLastPage() || TT.navigation.isCreditsPage()) {
    if (!TT.navigation.isCreditsPage() || (TT.navigation.isCreditsPage() && TT.navigation.isBookOpen())) {
      TT.pageflip.completeCurrentTurn();
      TT.navigation.goToCredits();
    }
    return false;
  }
  TT.pageflip.completeCurrentTurn();
  var currentPage = $("#pages section.current");
  var prevArticle, prevPage = null;
  if (TT.navigation.isHomePage()) {
    nextArticle = TT.navigation.classToArticle(currentPage.attr("class"));
    nextPage = TT.navigation.classToArticlePage(currentPage.attr("class"));
  } else {
    TT.pageflip.completeCurrentTurn();
    nextArticle = TT.navigation.classToArticle(currentPage.next("section").attr("class"));
    nextPage = TT.navigation.classToArticlePage(currentPage.next("section").attr("class"));
  }
  TT.navigation.goToPage(nextArticle, nextPage);
};
TT.navigation.goToHome = function(fromHistoryChange) {
  TT.tableofthings.hide();
  if (!TT.navigation.isHomePage()) {
    if (TT.navigation.isCreditsPage()) {
      TT.navigation.enqueueNavigation = {
        call: function() {
          delete this.call;
          setTimeout(TT.navigation.goToHome, 1);
        }
      };
      TT.navigation.goToPage(TT.history.THEEND, 1, false);
      return;
    }
    TT.navigation.currentPageName = TT.history.HOME;
    $("#back-cover").hide();
    $("body").removeClass("book").removeClass(TT.history.CREDITS).addClass(TT.history.HOME);
    TT.flipintro.activate();
    TT.sharing.updateSharer();
    TT.navigation.transitioningFromHardCover = false;
    $("#pages section").removeClass("current");
    $("#pages section").first().addClass("current");
    var currentPage = $("#pages section.current");
    currentPage.width(TT.PAGE_WIDTH);
    if (!fromHistoryChange) {
      // TT.history.pushState("/" + TT.locale.getLocaleCodeFromURL() + "/home");
      TT.history.pushState("/home");
    }
    TT.pageflip.turnToPage(currentPage, currentPage, -1, TT.pageflip.HARD_FLIP);
  }
};
TT.navigation.goToCredits = function(fromHistoryChange) {
  TT.tableofthings.hide();
  if (!TT.navigation.isCreditsPage() || (TT.navigation.isCreditsPage() && TT.navigation.isBookOpen())) {
    if ((TT.navigation.isBookOpen() || TT.navigation.isHomePage()) && (!TT.navigation.isLastPage() && !TT.navigation.isCreditsPage())) {
      TT.navigation.enqueueNavigation = {
        call: function() {
          delete this.call;
          setTimeout(TT.navigation.goToCredits, 1);
        }
      };
      TT.navigation.goToPage(TT.history.THEEND, 1, false);
      TT.paperstack.updateStack(1);
      return;
    }
    TT.navigation.currentPageName = TT.history.CREDITS;
    $("#page-shadow-overlay").hide();
    $("#front-cover").hide();
    $("#front-cover-bookmark").hide();
    $("#front-cover-arrow").hide();
    $("body").removeClass("book").removeClass(TT.history.HOME).addClass(TT.history.CREDITS);
    TT.sharing.updateSharer();
    TT.navigation.transitioningFromHardCover = false;
    $("#pages section").removeClass("current");
    $("#pages section").last().addClass("current");
    var currentPage = $("#pages section.current");
    TT.navigation.updatePageVisibility(currentPage, 1);
    if (!fromHistoryChange) {
      // TT.history.pushState("/" + TT.locale.getLocaleCodeFromURL() + "/credits");
      TT.history.pushState("/credits");
    }
    TT.pageflip.turnToPage(currentPage, currentPage, 1, TT.pageflip.HARD_FLIP);
  } else {
    $("#pages section.current").hide();
  }
};
TT.navigation.goToPage = function(articleId, pageNumber, fromHistoryChange) {
  TT.navigation.loadImages(articleId, pageNumber);
  if (TT.navigation.isCreditsPage() && articleId !== TT.history.THEEND) {
    TT.navigation.enqueueNavigation = {
      articleId: articleId,
      pageNumber: pageNumber,
      fromHistoryChange: fromHistoryChange,
      call: function() {
        delete this.call;
        TT.navigation.goToPage(this.articleId, this.pageNumber, this.fromHistoryChange);
      }
    };
    articleId = TT.history.THEEND;
    pageNumber = 1;
  }
  var currentPage = $("#pages section.current");
  var targetPage = $("#pages section.title-" + articleId + ".page-" + pageNumber);
  TT.navigation.hasNavigated = true;
  TT.tableofthings.hide();
  var isSamePageInBook = currentPage.attr("class") === targetPage.attr("class");
  var isSamePageOverall = targetPage.attr("class") === TT.navigation.currentPageName;
  if ((!isSamePageOverall && !isSamePageInBook) || (TT.navigation.isHomePage() || TT.navigation.isCreditsPage())) {
    TT.navigation.currentPageName = targetPage.attr("class");
    if (TT.navigation.classToArticle(TT.navigation.currentPageName) == TT.history.THEEND) {
      TT.sharing.updateSharer(true);
    }
    var type = TT.pageflip.SOFT_FLIP;
    if (TT.navigation.isHomePage() || TT.navigation.isCreditsPage()) {
      type = TT.pageflip.HARD_FLIP;
      TT.navigation.transitioningFromHardCover = true;
    }
    var currentGlobalPageNumber = TT.navigation.classToGlobalPage($(".current").attr("class"));
    var targetGlobalPageNumber = TT.navigation.classToGlobalPage(targetPage.attr("class"));
    if (currentGlobalPageNumber != null && targetGlobalPageNumber != null) {
      var steps = Math.abs(currentGlobalPageNumber - targetGlobalPageNumber);
      var direction = targetGlobalPageNumber > currentGlobalPageNumber ? 1 : -1;
      if (targetGlobalPageNumber == currentGlobalPageNumber) {
        direction = TT.navigation.isHomePage() ? 1 : -1;
      }
      TT.navigation.updatePageVisibility(targetPage, direction, steps);
      TT.pageflip.turnToPage(currentPage, targetPage, direction, type);
      if (!fromHistoryChange) {
        // TT.history.pushState("/" + TT.locale.getLocaleCodeFromURL() + "/" + articleId + "/" + pageNumber);
        TT.history.pushState("/" + articleId + "/" + pageNumber);
      }
      // TT.storage.setBookmark(articleId, pageNumber);
      TT.navigation.updateNextPrevLinks(targetPage);
      TT.navigation.updatePageReferences(articleId);
      return true;
    }
  }
  return false;
};
TT.navigation.updatePageVisibility = function(targetPage, direction, steps) {
  steps = steps || 0;
  var currentDepth = parseInt($("#pages section.current").css("z-index"));
  if (steps > 1 || TT.navigation.isHomePage()) {
    currentDepth = parseInt(targetPage.css("z-index"));
  }
  $("#pages section:not(.current)").each(function() {
    var z = parseInt($(this).css("z-index"));
    if (z > currentDepth) {
      $(this).width(0).hide().css("top");
    } else {
      if (z < currentDepth - 1) {
        $(this).hide();
      }
    }
  });
  targetPage.show();
  if (steps > 1 && direction == 1 && TT.navigation.isHomePage()) {
    $("#pages section.current").width(0).hide();
    targetPage.width(TT.PAGE_WIDTH).show();
  }
  if (!TT.navigation.isHomePage()) {
    $("#left-page").width(TT.BOOK_WIDTH_CLOSED).show();
  }
};

TT.navigation.updateStatsVisibility = function(targetPage, show) {
  var pageClasses = targetPage.attr("class").split(/\s+/);
  var pageNumber = 1;
  $.each( pageClasses, function(index, item) {
  	if (item.match("page-")) {
  		pageNumber = item.split('-')[1];
  	}
  	// Break from each
  	return !item.match("page-");
  });
  var infoBox = $("#piece-info .piece-" + pageNumber);
  if (!show) {
  	infoBox.hide();
  } else {
  	// Don't show if this is home, credits or end
  	if (!(TT.navigation.isHomePage() || TT.navigation.isCreditsPage() || TT.navigation.isLastPage()) && TT.navigation.isBookOpen()) {
  		infoBox.show();	
  	}
  }
};

TT.navigation.updateCurrentPointer = function(currentPage, targetPage) {
  if (TT.navigation.transitioningFromHardCover) {
    $("body").removeClass(TT.history.HOME).removeClass(TT.history.CREDITS).addClass("book");
    $("#page-shadow-overlay").hide();
    TT.navigation.transitioningFromHardCover = false;
  }
  currentPage.removeClass("current");
  targetPage.addClass("current");
  TT.sharing.updateSharer();
  TT.navigation.updateStatsVisibility(targetPage, true);
  TT.navigation.updatePageReferences();
  TT.navigation.updateNextPrevLinks(targetPage);
  if (TT.navigation.enqueueNavigation && TT.navigation.enqueueNavigation.call) {
    TT.navigation.enqueueNavigation.call();
    TT.navigation.enqueueNavigation = null;
  }
};
TT.navigation.updatePageReferences = function(articleId) {
  TT.chapternav.updateSelection(articleId);
  TT.tableofthings.updateSelection(articleId);
  TT.paperstack.updateStack();
  TT.illustrations.update($("#pages section.current"));
};
TT.navigation.cleanUpTransitions = function(currentPage, targetPage) {
  TT.pageflip.removeInactiveFlips();
  if (TT.pageflip.flips.length == 0) {
    TT.navigation.transitioningFromHardCover = false;
  }
};
TT.navigation.loadImages = function(articleId, pageNumber) {
  var cur = articleId && pageNumber ? $("#pages section.title-" + articleId + ".page-" + pageNumber) : $("#pages section.current");
  var pages = [cur];
  if (cur.prev("section").length) {
    pages.push(cur.prev("section"));
  }
  if (cur.next("section").length) {
    pages.push(cur.next("section"));
  }
  for (var i = 0; i < pages.length; i++) {
    pages[i].find("img").each(function() {
      if ($(this).attr("src") !== $(this).attr("data-src")) {
        $(this).attr("src", $(this).attr("data-src"));
      }
    });
  }
};
TT.cache = {};
TT.cache.initialize = function() {
  $(window.applicationCache).bind("downloading", TT.cache.onDownloadingHandler);
  $(window.applicationCache).bind("progress", TT.cache.onProgressHandler);
  $(window.applicationCache).bind("error", TT.cache.onErrorHandler);
  $(window.applicationCache).bind("cached", TT.cache.onCachedHandler);
  $(window.applicationCache).bind("updateready", TT.cache.onUpdateReadyHandler);
  $(window.applicationCache).bind("noupdate", TT.cache.onNoUpdateHandler);
  $(window.applicationCache).bind("obsolete", TT.cache.onObsoleteHandler);
};
TT.cache.onDownloadingHandler = function(event) {
  TT.log("TT.cache.onDownloadingHandler");
};
TT.cache.onNoUpdateHandler = function(event) {
  TT.log("TT.cache.onNoUpdateHandler");
};
TT.cache.onProgressHandler = function(event) {
  TT.log("TT.cache.onProgressHandler");
};
TT.cache.onErrorHandler = function(event) {
  TT.log("TT.cache.onErrorHandler");
};
TT.cache.onObsoleteHandler = function(event) {
  TT.log("TT.cache.onObsoleteHandler");
  window.location.reload();
};
TT.cache.onCachedHandler = function(event) {
  TT.log("TT.cache.onCachedHandler");
};
TT.cache.onUpdateReadyHandler = function(event) {
  TT.log("TT.cache.onCachedHandler");
  if (window.applicationCache.status == window.applicationCache.UPDATEREADY) {
    TT.log("Manifest is changed. New version being swapped in and reloading.");
    window.applicationCache.swapCache();
    window.location.reload();
  } else {
    TT.log("Manifest is unchanged. Do nothing.");
  }
};
TT.search = {};
TT.search.THING_RESULTS_LIMIT = 2;
TT.search.KEYWORD_RESULTS_LIMIT = 8;
TT.search.DEFAULT_TEXT = $("#search-field").attr("value");
TT.search.dropdown = null;
TT.search.dropdownResults = null;
TT.search.dropdownTitles = null;
TT.search.dropdownKeywords = null;
TT.search.field = null;
TT.search.hasFocus = false;
TT.search.titleResults = [];
TT.search.keywordResults = [];
TT.search.hideInterval = -1;
TT.search.initialize = function() {
  TT.search.field = $("#search-field");
  TT.search.dropdown = $("#search-dropdown");
  TT.search.dropdownResults = $("#search-dropdown div.results");
  TT.search.dropdownTitles = $("#search-dropdown div.results .things");
  TT.search.dropdownKeywords = $("#search-dropdown div.results .keywords");
  TT.search.field.focus(TT.search.onSearchFieldFocus);
  TT.search.field.blur(TT.search.onSearchFieldBlur);
  TT.search.field.change(TT.search.onSearchFieldChange);
  TT.search.field.keyup(TT.search.onSearchFieldChange);
  TT.search.field.click(function(event) {
    if (TT.search.field.val() == "") {
      TT.search.onSearchFieldChange(event);
    }
  });
};
TT.search.onSearchFieldFocus = function(event) {
  clearInterval(TT.search.hideInterval);
  if (event.target.value === TT.search.DEFAULT_TEXT) {
    event.target.value = "";
  }
  TT.search.showResult();
  TT.search.hasFocus = true;
  $("header, #search-dropdown").addClass("searching");
};
TT.search.onSearchFieldBlur = function(event) {
  clearInterval(TT.search.hideInterval);
  if (event.target.value === "") {
    event.target.value = TT.search.DEFAULT_TEXT;
  }
  TT.search.hideInterval = setInterval(TT.search.hideResults, 100);
  TT.search.hasFocus = false;
  $("header, #search-dropdown").removeClass("searching");
};
TT.search.onSearchFieldChange = function(event) {
  clearInterval(TT.search.hideInterval);
  if (TT.search.field.val() == "" || TT.search.field.val().length < 2) {
    TT.search.titleResults = [];
    TT.search.keywordResults = [];
    TT.search.hideResults();
  } else {
    TT.search.searchFor(TT.search.field.val());
  }
};
TT.search.searchFor = function(term) {
  TT.search.titleResults = [];
  TT.search.keywordResults = [];
  TT.search.regexEscape = function(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
  };
  var searchPattern = new RegExp(TT.search.regexEscape(term), "gi");
  $(".page h2, .page h3, .page p").each(function() {
    var elBeingSearched = $(this);
    var elText = $(this).text();
    if (searchPattern.test(elText)) {
      var matchVariations = elText.match(searchPattern);
      var uniqueMatchVariations = {};
      for (var i = 0; i < matchVariations.length; i++) {
        uniqueMatchVariations[matchVariations[i]] = true;
      }
      for (term in uniqueMatchVariations) {
        var elResults = elText.split(term);
        for (i = 1; i < elResults.length; i++) {
          var result = {};
          var anteSnippet = elResults[i - 1].substr(-10).replace(/</, "&lt;");
          var postSnippet = elResults[i].substr(0, 10).replace(/</, "&lt;");
          result.articleId = elBeingSearched.parents("section").eq(0).attr("class").match(/title-([a-z-0-9]+)/)[1];
          term = term.replace(/</, "&lt;");
          result.snippet = anteSnippet + "<strong>" + term + "</strong>" + postSnippet;
          var chapterElement = $("#chapter-nav ul li").find("[data-article=" + result.articleId + "]");
          if (chapterElement.length > 0) {
            result.articlePage = elBeingSearched.parents("section").eq(0).attr("class").match(/page-([0-9]+)/)[1];
            result.articleIndex = chapterElement.parent().index() + 1;
            result.articleTitle = chapterElement.attr("data-title");
            result.articleGlobalStartPage = $(".pageNumber", elBeingSearched.parents("section")).text();
            result.articleGlobalEndPage = chapterElement.attr("data-globalendpage");
            if (result.articleTitle.length > 38) {
              result.articleTitle = result.articleTitle.slice(0, 36) + "...";
            }
            if (elBeingSearched.is("h2") || elBeingSearched.is("h3")) {
              var isDuplicate = false;
              for (var j = 0; j < TT.search.titleResults.length; j++) {
                if (TT.search.titleResults[j].articleTitle == result.articleTitle) {
                  isDuplicate = true;
                }
              }
              if (!isDuplicate) {
                TT.search.titleResults.push(result);
              }
            } else {
              TT.search.keywordResults.push(result);
            }
          }
        }
      }
    }
  });
  TT.search.showResult();
};
TT.search.showResult = function() {
  TT.search.dropdownTitles.children("ul").remove();
  TT.search.dropdownKeywords.children("ul").remove();
  var hasTitleResults = TT.search.titleResults.length > 0;
  var hasKeywordResults = TT.search.keywordResults.length > 0;
  if (!hasTitleResults) {
    TT.search.dropdownTitles.hide();
  }
  if (!hasKeywordResults) {
    TT.search.dropdownKeywords.hide();
  }
  if (hasKeywordResults || hasTitleResults) {
    TT.search.dropdown.removeClass("no-results").addClass("open");
  } else {
    if (TT.search.field.val() != "") {
      TT.search.dropdown.addClass("no-results").addClass("open");
    }
  }
  if (hasTitleResults) {
    var resultHTML = $("<ul/>");
    for (var i = 0; i < Math.min(TT.search.titleResults.length, TT.search.THING_RESULTS_LIMIT); i++) {
      var result = TT.search.titleResults[i];
      var li = $("<li/>").mousedown(function() {
        TT.navigation.goToPage($(this).attr("class"), 1);
      });
      li.addClass(result.articleId);
      li.append('<div class="illustration"></div>');
      li.append('<p class="title">#' + result.articleIndex + " " + result.articleTitle + "</p>");
      if (Math.abs(parseInt(result.articleGlobalStartPage) - parseInt(result.articleGlobalEndPage)) != 0) {
        li.append('<p class="pages">' + SERVER_VARIABLES.PAGES + ": " + result.articleGlobalStartPage + "-" + result.articleGlobalEndPage + "</p>");
      } else {
        li.append('<p class="pages">' + SERVER_VARIABLES.PAGE + ": " + result.articleGlobalStartPage + "</p>");
      }
      resultHTML.append(li);
    }
    TT.search.dropdownTitles.append(resultHTML);
    TT.search.dropdownTitles.show();
  }
  if (hasKeywordResults) {
    var resultHTML = $("<ul/>");
    for (var i = 0; i < Math.min(TT.search.keywordResults.length, TT.search.KEYWORD_RESULTS_LIMIT); i++) {
      var result = TT.search.keywordResults[i];
      var li = $("<li/>").mousedown(function() {
        TT.navigation.goToPage($(this).attr("data-articleId"), $(this).attr("data-articlePage"));
      });
      li.attr("data-articleId", result.articleId);
      li.attr("data-articlePage", result.articlePage);
      li.append('<p class="snippet">"...' + result.snippet + '..."</p>');
      li.append('<p class="pages">' + SERVER_VARIABLES.THING + " #" + result.articleIndex + " " + SERVER_VARIABLES.PAGE + ": " + result.articleGlobalStartPage + "</p>");
      resultHTML.append(li);
    }
    TT.search.dropdownKeywords.append(resultHTML);
    TT.search.dropdownKeywords.show();
  }
  TT.search.dropdown.children(".fader").height(TT.search.dropdownResults.outerHeight());
};
TT.search.hideResults = function() {
  TT.search.dropdown.removeClass("open");
};
TT.chapternav = {};
TT.chapternav.initialize = function() {
  $("#chapter-nav ul li").click(TT.chapternav.onChapterClick);
  if (!TT.IS_TOUCH_DEVICE) {
    $("#chapter-nav ul li").mouseover(TT.chapternav.onChapterMouseOver);
    $("#chapter-nav ul li").mouseout(TT.chapternav.onChapterMouseOut);
  }
  $("#chapter-nav ul li .over div.description").css({
    opacity: 0
  });
};
TT.chapternav.updateReadMarkers = function() {
  $("#chapter-nav ul li").each(function() {
    var articleId = $("a", this).attr("data-article");
    if (TT.storage.hasArticleBeenRead(articleId)) {
      $(this).addClass("read");
    }
  });
};
TT.chapternav.getDisabledArticles = function() {
  var articles = [];
  $("#chapter-nav ul li.disabled").each(function() {
    var article = $("a", this).attr("data-article");
    if (article) {
      articles.push(article);
    }
  });
  return articles;
};
TT.chapternav.updateSelection = function(overrideArticleId) {
  var selectedArticleId = TT.navigation.classToArticle($("#pages section.current").attr("class"));
  if (overrideArticleId) {
    selectedArticleId = overrideArticleId;
  }
  $("#chapter-nav ul li").removeClass("selected");
  if (selectedArticleId && !TT.navigation.isHomePage() && !TT.navigation.isCreditsPage() && !TT.navigation.isForeword()) {
  	TT.sharing.updateSharerIndex(TT.chapternav.getProgress());
    // var element = $("#chapter-nav ul li").find("[data-article=" + selectedArticleId + "]");
    // if (element && element.parent()) {
      // element.parent().addClass("selected");
      // TT.sharing.updateSharerIndex(element.parent().index() + 1);
    // }
  }
  if (!TT.storage.isFirstTimeVisitor || !TT.navigation.isHomePage() || TT.navigation.hasNavigated) {
    $("#chapter-nav").show();
  }
  $("#chapter-nav ul li a.over").each(function() {
    $(this).css({
      top: -$(this).height() + 4
    });
  });
};
TT.chapternav.getProgress = function(overrideArticleId) {
  // When navigation is not implemented
  return Math.max(TT.navigation.classToArticlePage($("#pages section.current").attr("class")), 1);
  
  // When navigation is implemented
  var selectedArticle = $("#chapter-nav ul li.selected");
  if (overrideArticleId) {
    selectedArticle = $("#chapter-nav ul li").find("[data-article=" + overrideArticleId + "]").parent();
  }
  if (TT.navigation.isHomePage() || TT.navigation.isForeword()) {
  	TT.log("isHomePage");
    return 0;
  } else {
  	TT.log("isCreditsPage");
    if (TT.navigation.isCreditsPage() || TT.navigation.isLastPage() || selectedArticle.length == 0) {
      return 1;
    }
  }

  return Math.min(selectedArticle.index() / ($("#chapter-nav ul li:not(.disabled)").length - 1), 1);
};
TT.chapternav.onChapterClick = function(event) {
  var item = $(event.target).is("li") ? $(event.target) : $(event.target).parents("li");
  var articleId = $("a", item).attr("data-article");
  if (articleId && !item.hasClass("disabled")) {
    if (TT.navigation.goToPage(articleId, 1)) {
      if (TT.chapternav.getProgress(articleId) > TT.chapternav.getProgress()) {
        TT.paperstack.updateStack(TT.chapternav.getProgress(articleId));
      }
      TT.chapternav.updateSelection(articleId);
    }
  }
  event.preventDefault();
};
TT.chapternav.onChapterMouseOver = function(event) {
  var item = $(event.target).is("li") ? $(event.target) : $(event.target).parents("li");
  var description = $("div.description", item);
  description.stop(true, false).fadeTo(200, 1);
};
TT.chapternav.onChapterMouseOut = function(event) {
  var item = $(event.target).is("li") ? $(event.target) : $(event.target).parents("li");
  var description = $("div.description", item);
  description.fadeTo(200, 0);
};
TT.sharing = {};
var l = window.location;
TT.sharing.BASE_URL = l.protocol + "//" + l.hostname + "/" + SERVER_VARIABLES.LANG;
TT.sharing.FACEBOOK_SHARER = "http://www.facebook.com/sharer.php";
TT.sharing.TWITTER_SHARER = "http://twitter.com/share";
TT.sharing.PLUSONE_SHARER = "http://www.20thingsilearned.com/" + SERVER_VARIABLES.LANG;
TT.sharing.initialize = function() {
  $("footer div.sharing .facebook, #credits div.share .facebook").click(TT.sharing.shareBookOnFacebook);
  $("footer div.sharing .twitter, #credits div.share .twitter").click(TT.sharing.shareBookOnTwitter);
  $("footer div.sharing .url").click(TT.sharing.openClipboardNotification);
  $("#sharer div.content ul li.facebook").click(TT.sharing.shareChapterOnFacebook);
  $("#sharer div.content ul li.twitter").click(TT.sharing.shareChapterOnTwitter);
  // $("#sharer div.content ul li.print").click(TT.sharing.printThing);
  // TT.sharing.updateGlobalGplusBtn();
  $(document).mousedown(TT.sharing.documentMouseDownHandler);
};
TT.sharing.updateSharer = function(hide) {
  var articleId = TT.navigation.classToArticle($("#pages section.current").attr("class"));
  $("#sharer div.content ul li.print a").attr("href", "/" + SERVER_VARIABLES.LANG + "/" + articleId + "/print");
  if (TT.navigation.isHomePage() || TT.navigation.isCreditsPage() || TT.navigation.isLastPage() || TT.navigation.isForeword() || hide) {
    $("#sharer").stop(true, true);
    $("#sharer").fadeOut(150);
  } else {
    if (TT.navigation.currentThing != articleId) {
      TT.navigation.currentThing = articleId;
      TT.sharing.updateChapterGplusBtn();
    }
    $("#sharer").stop(true, true).delay(150).fadeIn(150);
  }
};
TT.sharing.updateChapterGplusBtn = function() {
  // var li = $("#sharer li.gplus").html("");
  // var url = TT.sharing.PLUSONE_SHARER + "/" + TT.navigation.getCurrentArticleId();
  // var newBtn = '<g:plusone size="small" count="false" href="' + url + '"></g:plusone>';
  // li.append(newBtn);
  // gapi.plusone.go(li[0]);
};
TT.sharing.updateGlobalGplusBtn = function() {
  // var url = TT.sharing.PLUSONE_SHARER;
  // var footerLi = $("footer .sharing li.gplus");
  // var footerBtn = '<g:plusone size="small" count="false" href="' + url + '"></g:plusone>';
  // footerLi.append(footerBtn);
  // gapi.plusone.go(footerLi[0]);
  // var creditsLi = $("#credits .share li.gplus");
  // var creditsBtn = '<g:plusone count="false" href="' + url + '"></g:plusone>';
  // creditsLi.append(creditsBtn);
  // gapi.plusone.go(creditsLi[0]);
};
TT.sharing.updateSharerIndex = function(index) {
  if (index != 0) {
    if (index != $("#sharer div.content p.index span").text()) {
      $("#sharer div.content p.index span").each(function(i) {
        if (i > 1) {
          $(this).remove();
        }
      });
      $("#sharer div.content p.index span").delay(300).fadeOut(200, function() {
        $(this).remove();
      });
      var span = $("<span>" + index + "</span>");
      span.hide().delay(300).fadeIn(200);
      $("#sharer div.content p.index").append(span);
      TT.sharing.updateSharer();
    }
  } else {
    $("#sharer").fadeOut();
  }
};
TT.sharing.openClipboardNotification = function() {
  $("footer .clipboard-notification").show().focus().select();
  return false;
};
TT.sharing.documentMouseDownHandler = function(event) {
  if (event && event.target === $("footer .clipboard-notification")[0]) {
    $("footer .clipboard-notification").focus().select();
    return false;
  } else {
    $("footer .clipboard-notification").fadeOut(200);
  }
};
TT.sharing.shareBookOnFacebook = function() {
  // var url = TT.sharing.BASE_URL;
  var url = window.location.href;
  var title = SERVER_VARIABLES.FACEBOOK_MESSAGE;
  TT.sharing.shareOnFacebook(url, title);
  return false;
};
TT.sharing.shareBookOnTwitter = function() {
  // var url = TT.sharing.BASE_URL;
  var url = window.location.href;
  var title = SERVER_VARIABLES.TWITTER_MESSAGE;
  TT.sharing.shareOnTwitter(url, title);
  return false;
};
TT.sharing.shareChapterOnFacebook = function() {
  // var url = TT.sharing.BASE_URL + "/" + TT.navigation.getCurrentArticleId();
  var url = window.location.href;
  var title = SERVER_VARIABLES.FACEBOOK_MESSAGE_SINGLE;
  TT.sharing.shareOnFacebook(url, title);
  return false;
};
TT.sharing.shareChapterOnTwitter = function() {
  // var url = TT.sharing.BASE_URL + "/" + TT.navigation.getCurrentArticleId();
  var url = window.location.href;
  var title = SERVER_VARIABLES.TWITTER_MESSAGE_SINGLE;
  TT.sharing.shareOnTwitter(url, title);
  return false;
};
TT.sharing.shareOnFacebook = function(url, title) {
  var shareURL = TT.sharing.FACEBOOK_SHARER;
  shareURL += "?u=" + encodeURIComponent(url);
  shareURL += "&t=" + encodeURIComponent(title);
  TT.log(shareURL);
  window.open(shareURL, "Facebook", "toolbar=0,status=0,width=726,location=no,menubar=no,height=436");
};
TT.sharing.shareOnTwitter = function(url, title) {
  var shareURL = TT.sharing.TWITTER_SHARER;
  shareURL += "?original_referer=" + encodeURIComponent(url);
  shareURL += "&text=" + encodeURIComponent(title);
  shareURL += "&url=" + encodeURIComponent(url);
  window.open(shareURL, "Twitter", "toolbar=0,status=0,width=726,location=no,menubar=no,height=436");
};
TT.overlay = {};
TT.overlay.overlay = null;
TT.overlay.bookmark = null;
TT.overlay.print = null;
TT.overlay.visible = false;
TT.overlay.initialize = function() {
  TT.overlay.overlay = $("#overlay");
  TT.overlay.bookmark = $("#overlay div.bookmark");
  TT.overlay.print = $("#overlay div.print");
};
TT.overlay.showBookmark = function(continueCallback, restartCallback, cancelCallback) {
  TT.overlay.overlay.stop().fadeIn(200);
  TT.overlay.bookmark.siblings().hide();
  TT.overlay.bookmark.stop().fadeIn(200);
  $("a.resume", TT.overlay.bookmark).click(function() {
    TT.overlay.hide();
    continueCallback();
    return false;
  });
  $("a.restart", TT.overlay.bookmark).click(function() {
    TT.overlay.hide();
    restartCallback();
    return false;
  });
  $("a.close", TT.overlay.bookmark).click(function() {
    TT.overlay.hide();
    cancelCallback();
    return false;
  });
  TT.overlay.visible = true;
  TT.overlay.hasShownBookmark = true;
  TT.pageflip.unregisterEventListeners();
  $("body").addClass("overlay");
};
TT.overlay.showPrint = function() {
  TT.overlay.overlay.stop().fadeIn("fast");
  TT.overlay.print.siblings().hide();
  TT.overlay.print.stop().fadeIn("fast");
  $("a.close", TT.overlay.print).click(function() {
    TT.overlay.hide();
    return false;
  });
  $("a.downloadPdf.disabled", TT.overlay.print).click(function() {
    return false;
  });
  TT.overlay.visible = true;
  TT.pageflip.unregisterEventListeners();
  $("body").addClass("overlay");
};
TT.overlay.hide = function() {
  TT.overlay.overlay.stop().fadeOut("fast");
  TT.overlay.bookmark.stop().fadeOut("fast");
  TT.overlay.print.stop().fadeOut("fast");
  TT.overlay.visible = false;
  TT.pageflip.registerEventListeners();
  $("body").removeClass("overlay");
};
TT.tableofthings = {};
TT.tableofthings.COLUMNS = 5;
TT.tableofthings.visible = false;
TT.tableofthings.initialize = function() {
  $("#table-of-contents ul li").mouseenter(TT.tableofthings.onChapterMouseOver);
  $("#table-of-contents ul li").mouseleave(TT.tableofthings.onChapterMouseOut);
  $("#table-of-contents ul li").click(TT.tableofthings.onChapterClick);
};
TT.tableofthings.updateReadMarkers = function() {
  $("#table-of-contents ul li").each(function() {
    var articleId = $("a", this).attr("data-article");
    if (TT.storage.hasArticleBeenRead(articleId)) {
      $(this).addClass("read");
    }
  });
};
TT.tableofthings.updateSelection = function(overrideArticleId) {
  var selectedArticleId = TT.navigation.classToArticle($("#pages section.current").attr("class"));
  if (overrideArticleId) {
    selectedArticleId = overrideArticleId;
  }
  $("#table-of-contents ul li").removeClass("selected");
  if (selectedArticleId) {
    var element = $("#table-of-contents ul li").find("[data-article*=" + selectedArticleId + "]");
    if (element && element.parent()) {
      element.parents("li").addClass("selected");
    }
  }
};
TT.tableofthings.show = function() {
  if (!TT.tableofthings.visible) {
    $("body").addClass("tot");
    $("#table-of-contents").stop(true, true).show().fadeTo(200, 1);
    $("#table-of-contents div.header").stop().css({
      opacity: 1
    });
    TT.tableofthings.truncate();
    $("#table-of-contents ul li").each(function(i) {
      var row = Math.floor(i / TT.tableofthings.COLUMNS);
      var col = i % TT.tableofthings.COLUMNS;
      row++;
      col++;
      $(this).stop().css({
        opacity: 0
      }).show().delay((row + col) * 50).fadeTo(100, 1);
    });
    TT.updateLayout();
  }
  TT.tableofthings.visible = true;
  TT.pageflip.unregisterEventListeners();
};
TT.tableofthings.hide = function() {
  $("body").removeClass("tot");
  $("#table-of-contents").delay(200).fadeTo(200, 0, function() {
    $(this).hide();
  });
  $("#table-of-contents div.header").stop().fadeTo(150, 0);
  var length = $("#table-of-contents ul li").length;
  $("#table-of-contents ul li").each(function(i) {
    var row = Math.floor((length - 1 - i) / TT.tableofthings.COLUMNS);
    var col = (length - 1 - i) % TT.tableofthings.COLUMNS;
    row++;
    col++;
    $(this).stop().fadeTo((row + col) * 40, 0);
  });
  TT.tableofthings.visible = false;
  if (!TT.navigation.isFullScreen()) {
    TT.pageflip.registerEventListeners();
  }
  TT.updateLayout();
};
TT.tableofthings.onChapterClick = function(event) {
  if ($("body").hasClass("tot")) {
    var articleId = $(event.target).parents("li").children("a").attr("data-article");
    if (!articleId) {
      articleId = $(event.target).children("a").attr("data-article");
    }
    if (TT.navigation.goToPage(articleId, 1)) {
      TT.tableofthings.hide();
      TT.chapternav.updateSelection(articleId);
      TT.tableofthings.updateSelection(articleId);
    }
  }
  return false;
};
TT.tableofthings.onChapterMouseOver = function(event) {
  $(this).find(".extended").show();
  $(this).find(".ellipsis").hide();
  $(this).find("p.fullyTruncated").show();
  if ($(event.target).parents("li").hasClass("disabled") || $(event.target).parents("li").hasClass("selected")) {
    return false;
  }
};
TT.tableofthings.onChapterMouseOut = function(event) {
  $(this).find(".extended").hide();
  $(this).find(".ellipsis").show();
  $(this).find("p.fullyTruncated").hide();
};
TT.tableofthings.truncate = function() {
  $("#table-of-contents ul li").each(function(i) {
    var that = $(this);
    var thatA = that.find("a");
    that.css("z-index", 1000 - i);
    if (thatA.outerHeight() > 130) {
      TT.tableofthings.findSliceLength(thatA);
    }
  });
};
TT.tableofthings.findSliceLength = function(aEl) {
  var p = aEl.find("p").eq(1);
  var len = p.text().length;
  var txt = p.text();
  var start = len;
  while (aEl.outerHeight() > 130) {
    len = start = txt.lastIndexOf(" ", start - 1);
    if (len <= 0) {
      len = 0;
    }
    var tease = txt.slice(0, len);
    var extended = txt.slice(len);
    var ellipsis = extended.length > 0 && len != 0 ? " ..." : "";
    p.html('<span class="tease">' + tease + '</span><span class="ellipsis">' + ellipsis + '</span><span class="extended" style="display:none;">' + extended + "</span>");
    if (len == 0) {
      p.addClass("fullyTruncated").hide();
      break;
    }
  }
  var h3 = aEl.find("h3");
  len = h3.text().length;
  txt = h3.text();
  var start = len;
  while (aEl.outerHeight() > 130) {
    len = start = txt.lastIndexOf(" ", start - 1);
    var tease = txt.slice(0, len);
    var extended = txt.slice(len);
    var ellipsis = extended.length > 0 ? " ..." : "";
    h3.html('<span class="tease">' + tease + '</span><span class="ellipsis">' + ellipsis + '</span><span class="extended" style="display:none;">' + extended + "</span>");
  }
};
TT.flipintro = {};
TT.flipintro.WIDTH = 89;
TT.flipintro.HEIGHT = 29;
TT.flipintro.VSPACE = 20;
TT.flipintro.loopInterval = -1;
TT.flipintro.canvas = null;
TT.flipintro.context = null;
TT.flipintro.flip = {
  progress: 0,
  alpha: 0
};
TT.flipintro.initialize = function() {
  TT.flipintro.canvas = $("#flip-intro");
  if (TT.flipintro.canvas[0]) {
    TT.flipintro.canvas[0].width = TT.flipintro.WIDTH;
    TT.flipintro.canvas[0].height = TT.flipintro.HEIGHT + (TT.flipintro.VSPACE * 2);
    TT.flipintro.context = TT.flipintro.canvas[0].getContext("2d");
  }
};
TT.flipintro.activate = function() {
  if (TT.flipintro.loopInterval == -1) {
    TT.flipintro.flip.progress = 1;
    TT.flipintro.loopInterval = setInterval(TT.flipintro.render, 32);
  }
};
TT.flipintro.deactivate = function() {
  clearInterval(TT.flipintro.loopInterval);
  TT.flipintro.loopInterval = -1;
};
TT.flipintro.render = function() {
  if (!TT.flipintro.canvas[0]) {
    return;
  }
  TT.flipintro.context.clearRect(0, 0, TT.flipintro.WIDTH, TT.flipintro.HEIGHT + (TT.flipintro.VSPACE * 2));
  if (!TT.navigation.isHomePage()) {
    TT.flipintro.deactivate();
  }
  TT.flipintro.flip.progress -= Math.max(0.12 * (1 - Math.abs(TT.flipintro.flip.progress)), 0.02);
  TT.flipintro.flip.alpha = 1 - ((Math.abs(TT.flipintro.flip.progress) - 0.7) / 0.3);
  if (TT.flipintro.flip.progress < -2) {
    TT.flipintro.flip.progress = 1;
  }
  var strength = 1 - Math.abs(TT.flipintro.flip.progress);
  var anchorOutdent = strength * 12;
  var controlOutdent = strength * 8;
  var source = {
    top: {
      x: TT.flipintro.WIDTH * 0.5,
      y: TT.flipintro.VSPACE
    },
    bottom: {
      x: TT.flipintro.WIDTH * 0.5,
      y: TT.flipintro.HEIGHT + TT.flipintro.VSPACE
    }
  };
  var destination = {
    top: {
      x: source.top.x + (TT.flipintro.WIDTH * TT.flipintro.flip.progress * 0.6),
      y: TT.flipintro.VSPACE - anchorOutdent
    },
    bottom: {
      x: source.bottom.x + (TT.flipintro.WIDTH * TT.flipintro.flip.progress * 0.6),
      y: TT.flipintro.HEIGHT + TT.flipintro.VSPACE - anchorOutdent
    }
  };
  var control = {
    top: {
      x: source.top.x + (12 * TT.flipintro.flip.progress),
      y: TT.flipintro.VSPACE - controlOutdent
    },
    bottom: {
      x: source.bottom.x + (12 * TT.flipintro.flip.progress),
      y: TT.flipintro.HEIGHT + TT.flipintro.VSPACE - controlOutdent
    }
  };
  TT.flipintro.context.fillStyle = "rgba(238,238,238," + TT.flipintro.flip.alpha + ")";
  TT.flipintro.context.strokeStyle = "rgba(90,90,90," + TT.flipintro.flip.alpha + ")";
  TT.flipintro.context.beginPath();
  TT.flipintro.context.moveTo(source.top.x, source.top.y);
  TT.flipintro.context.quadraticCurveTo(control.top.x, control.top.y, destination.top.x, destination.top.y);
  TT.flipintro.context.lineTo(destination.bottom.x, destination.bottom.y);
  TT.flipintro.context.quadraticCurveTo(control.bottom.x, control.bottom.y, source.bottom.x, source.bottom.y);
  TT.flipintro.context.fill();
  TT.flipintro.context.stroke();
};
var TT = TT || {};
TT.locale = {};
TT.locale.title = null;
TT.locale.list = null;
TT.locale.initialize = function() {
  this.title = $("#language-selector-title");
  this.list = $("#language-selector-list");
  this.title.click(function() {
    if ($(this).hasClass("open")) {
      TT.locale.closeList();
    } else {
      TT.locale.openList();
    }
  });
  $("li a", this.list).attr("href", "#").click(function(event) {
    var targetLocale = $(this).parents("li").attr("data-locale");
    var targetURL = TT.locale.removeLocaleCodeFromURL(document.location.pathname);
    document.location = "/" + targetLocale + targetURL;
    event.preventDefault();
  });
  this.title.mousedown(function(event) {
    event.preventDefault();
  });
};
TT.locale.onDocumentMouseDown = function(event) {
  if ($(event.target).parents("#language-selector").length === 0) {
    TT.locale.closeList();
  }
};
TT.locale.openList = function() {
  this.title.addClass("open");
  this.list.addClass("open");
  $(document).bind("mousedown", this.onDocumentMouseDown);
};
TT.locale.closeList = function() {
  this.title.removeClass("open");
  this.list.removeClass("open");
  $(document).unbind("mousedown", this.onDocumentMouseDown);
};
TT.locale.getLocaleCodeFromURL = function() {
  var code = document.location.pathname;
  if (code.indexOf("fil-PH") > 0) {
    code = code.match(/\/fil-PH/gi) || "";
  } else {
    if (code.indexOf("es-419") > 0) {
      code = code.match(/\/es-419/gi) || "";
    } else {
      code = code.match(/\/(..\-..)/gi) || "";
    }
  }
  code = code.toString().replace(/\//gi, "");
  if (!code) {
    return "en-US";
  }
  return code;
};
TT.locale.getLanguageFromLocaleCode = function(localeCode) {
  var languageCode = localeCode.slice(0, localeCode.indexOf("-"));
  if (!languageCode) {
    return locale;
  }
  return languageCode;
};
TT.locale.removeLocaleCodeFromURL = function(url) {
  if (url.indexOf("fil-PH") > 0) {
    return url.replace(/\/fil-PH/gi, "");
  } else {
    if (url.indexOf("es-419") > 0) {
      return url.replace(/\/es-419/gi, "");
    } else {
      return url.replace(/\/(..\-..)/gi, "");
    }
  }
};