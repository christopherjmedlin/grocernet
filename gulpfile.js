var gulp = require('gulp')
var pjson = require('./package.json')
var del = require('del')
var sass = require('gulp-sass')
var plumber = require('gulp-plumber')
var uglify = require('gulp-uglify')
var concat = require('gulp-concat')
var rename = require('gulp-rename')
var imagemin = require('gulp-imagemin')
var exec = require('gulp-exec')
var runSequence = require('run-sequence')

// inspired by this boilerplate:
// https://github.com/hypebeast/flask-gulp-starter-kit/
//
// thanks hypebeast!

var pathsConfig = function(appName) {
    this.app = "./" + (appName || pjson.name);

    return {
        app: this.app,
        templates: this.app + '/templates',
        sass: this.app + '/static/sass',
        fonts: this.app + '/static/fonts',
        images: this.app + '/static/img',
        js: this.app + '/static/js',
        components: this.app + '/static/components',
        dist: {
            js: this.app + '/static/dist/js',
            css: this.app + '/static/dist/css',
            images: this.app + '/static/dist/img',
        }
    }
};

var paths = pathsConfig();

gulp.task("clean", function() {
    return del([paths.app + '/static/dist']);
});

gulp.task("sass", function() {
    return gulp.src(paths.sass + '/style.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(rename('app.min.css'))
        .pipe(gulp.dest(paths.dist.css));
});

gulp.task("js", function() {
    return gulp.src(paths.js + "/*.js")
        .pipe(plumber())
        .pipe(uglify())
        .pipe(concat('app.min.js'))
        .pipe(gulp.dest(paths.dist.js));
});

gulp.task("img", function() {
    return gulp.src(paths.images + "/*")
        .pipe(imagemin())
        .pipe(gulp.dest(paths.dist.images))
});

gulp.task("build", function () {
    runSequence("clean", "sass", "js", "img");
});

gulp.task('watch', function () {
    gulp.watch(paths.sass + '/**/*.scss', ['sass']);
    gulp.watch(paths.js + '/**/*.js', ['js']);
    gulp.watch(paths.images + '/*', ['img']);
});

gulp.task("default", function () {
    runSequence("build", "watch");
});


