
log.i <- function(format, ...){
  cat(sprintf(format, ...))
}


checkDirAndCreateIfNotExist <- function(directory) {
  if (!dir.exists(directory)){
    dir.create(directory)
  }
}


checkOpt <- function(opt, arg, required=TRUE){
  if (!is.na(opt[[arg]]) || required==FALSE) {
    opt[[arg]]
  } else {
    stop(sprintf("%s parameter must be provided. See script usage (--help)", opt[[arg]]))
  }
}
