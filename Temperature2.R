n <- 1000
m <- 4
delta_t_values <- vector()
val <- 0.01
table <- data.frame(delta_t = numeric(), mean_max_temp = numeric(), var_max_temp = numeric())

# Generate delta_t values
for (i in 1:m) {
  delta_t_values <- c(delta_t_values, val)
  val <- val / 10
}

# Set up plotting area
par(mfrow = c(2, length(delta_t_values) / 2))

# Loop over delta_t values
for (delta_t in delta_t_values) {
  p <- numeric(n)  # Preallocate vector for maximum temperatures
  
  # Simulate n random walks
  for (i in 1:n) {
    max_temp_t <- 0
    max_temp <- 0
    temp <- 0
    
    # Random walk
    for (t in 1:(1 / delta_t)) {
      temp_increase <- rnorm(1, mean = 0, sd = sqrt(delta_t))
      temp <- temp + temp_increase
      if (temp >= max_temp) {
        max_temp <- temp
        max_temp_t<-t*delta_t
      }
    }
    p[i] <- max_temp_t
  }
  
  # Calculate summary statistics
  mean_max_temp <- mean(p)
  var_max_temp <- var(p)
  
  # Append to table
  table <- rbind(table, data.frame(delta_t = delta_t, mean_max_temp = mean_max_temp, var_max_temp = var_max_temp))
  
 
  # Compute histogram with probabilities
  hist_data <- hist(
    p, breaks = 30, plot = FALSE  # Get histogram data without plotting
  )
  normalized_counts <- hist_data$counts / sum(hist_data$counts)  # Normalize to probabilities
  
  # Plot the normalized histogram
  plot(
    hist_data$mids, normalized_counts, type = "h", lwd = 10, col = "lightblue",
    main = paste("Distribution of T_max (delta_t =", delta_t, ")"),
    xlab = "T_max", ylab = "Probability", ylim = c(0, max(normalized_counts))
  )
  
  # Compute density curve and rescale to match histogram scale
  dens <- density(p)
  scaled_density <- dens$y * (sum(normalized_counts) * diff(hist_data$breaks)[1])
  
  # Overlay rescaled density curve
  lines(dens$x, scaled_density, col = "red", lwd = 2)
  
  # Add legend
  legend("top", legend = c("Normalized Histogram", "Scaled Density Curve"),
         col = c("lightblue", "red"), lty = c(1, 1), lwd = c(10, 2))
  
  
}
# Print summary statistics table
print(table)

