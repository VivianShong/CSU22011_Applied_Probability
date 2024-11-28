n <- 1000
m <- 4
delta_t_values <- vector()
val <- 0.01

# Create delta_t values by successively dividing val by 10
for(i in 1:m) {
  delta_t_values <- c(delta_t_values, val)
  val <- val / 10
}

# Initialize data frame for summary statistics
summary_stats <- data.frame(delta_t = numeric(), mean_proportion = numeric(), var_proportion = numeric())

# Initialize plot layout
par(mfrow = c(2, ceiling(length(delta_t_values) / 2)))

# Loop over each delta_t value
for(delta_t in delta_t_values) {
  # Initialize p for each delta_t
  p <- numeric(n)  # Preallocate for efficiency
  
  # Run n simulations for each delta_t
  for(i in 1:n) {
    count <- 0
    temp <- 0
    
    # Track temperature changes over time intervals (1 / delta_t steps)
    for(t in 1:(1 / delta_t)) {
      temp_increase <- rnorm(1, mean = 0, sd = sqrt(delta_t))  # Use sqrt(delta_t) for accurate scaling
      temp <- temp + temp_increase
      if (temp > 0) count <- count + 1
    }
    
    # Store the proportion of positive temperatures
    p[i] <- count * delta_t
  }
  
  # Calculate summary statistics
  mean_proportion <- mean(p)
  var_proportion <- var(p)
  
  # Append summary statistics to data frame
  summary_stats <- rbind(summary_stats, data.frame(delta_t = delta_t, mean_proportion = mean_proportion, var_proportion = var_proportion))
  
  # Compute histogram with probabilities
  hist_data <- hist(
    p, breaks = 30, plot = FALSE  # Get histogram data without plotting
  )
  normalized_counts <- hist_data$counts / sum(hist_data$counts)  # Normalize to probabilities
  
  # Plot the normalized histogram
  plot(
    hist_data$mids, normalized_counts, type = "h", lwd = 10, col = "lightblue",
    main = paste("Distribution of P (delta_t =", delta_t, ")"),
    xlab = "P", ylab = "Probability", ylim = c(0, max(normalized_counts))
  )
  
  # Compute density curve and rescale to match histogram scale
  dens <- density(p)
  scaled_density <- dens$y * (sum(normalized_counts) * diff(hist_data$breaks)[1])
  
  # Overlay rescaled density curve
  lines(dens$x, scaled_density, col = "red", lwd = 2)
  
  legend("top", legend = c("Normalized Histogram", "Scaled Density Curve"),
         col = c("lightblue", "red"), lty = c(1, 1), lwd = c(10, 2), 
         xpd = TRUE, inset = c(-0.3, 0))  # inset moves the legend outside to the right
  
}

# Print summary statistics table
print(summary_stats)


