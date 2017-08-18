fs <- read.csv("featureOutput.csv",header=TRUE)

# Extract feature matrix (i.e. remove the first column)
f <- fs[, -(1)]
names <- fs[,1]

# Compute the principal components of the feature matrix
# Note that p$scores contains the actual loadings
p <- princomp(na.omit(as.matrix(f)), cor = TRUE)

# Average the first two principal components of all the songs for each
# song into a single XY point
d <- aggregate(p$scores[, 1:2], by = list(songName = fs$songName), mean)
names(d) <- c("track", "x", "y")

# Define the color of the region for each song.
# First scale the X and Y coordinates of the songs to lie in [0, 1]
scale01 <- function(x) (x - min(x)) / (max(x) - min(x))
xs <- scale01(d$x)
ys <- scale01(d$y)
# Then use these as the Red and Green components, with Blue fixed at 1
song_color <- rgb(xs, ys, 1)

# Set up a new graphics window with no borders
dev.new()
par(mai = c(0, 0, 0, 0))

png(file="output.png",width=1920,height=1080)

# Draw an empty plot
plot(d$x, d$y, lwd=0.2,type = "n")

# Load the deldir package to perform Voronoi tesselations
library(deldir)

# Compute and plot the Voronoi region for each song
regions <- tile.list(deldir(d))
for(k in 1:length(regions)) {
  polygon(regions[[k]], col = song_color[k], lwd = 0.01)
  text(mean(regions[[k]]$x),mean(regions[[k]]$y),names[k])
}

dev.off()
