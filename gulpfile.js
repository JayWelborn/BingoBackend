const autoprefixer = require('autoprefixer');
const browserSync  = require('browser-sync').create();
const concat       = require('gulp-concat');
const gulp         = require('gulp');
const postcss      = require('gulp-postcss');
const sass         = require('gulp-sass');
const reload       = browserSync.reload;
const sourcemaps   = require('gulp-sourcemaps');

// Start Django server
gulp.task('django', function() {
    const spawn = require('child_process').spawn;
    return spawn('python', ['bingo/manage.py', 'runserver'])
        .stderr.on('data', (data) => {
        console.log(`${data}`);
    });
});

// Process sass files and output prefixed css
gulp.task('styles', function() {
    gulp.src('./bingo/**/main.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('style.css'))
        .pipe(sourcemaps.init())
        .pipe(postcss([autoprefixer() ]))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./bingo/home/static/css/'));
});

gulp.task('browsersync', function() {
    browserSync.init({
        notify: true,
        proxy: "localhost:8000",
        browser: ["google chrome", "firefox"]
    });
});

// Tell gulp to execute 'styles' every time a sass file changes
gulp.task('watch', function() {
    gulp.watch('./**/*.{sass,scss}', ['styles']);
    gulp.watch(['./**/*.{sass,scss,css,html,py,js}'], reload);
});

// Start django server and start watching sass files
gulp.task('default', ['django', 'browsersync', 'watch']);
