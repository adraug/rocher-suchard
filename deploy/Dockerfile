# syntax=docker/dockerfile:1

# Build the Linux Packwiz binary from the same revision used on the maintainer's
# machine. Packwiz has no release tags, so this Git revision is intentional.
FROM golang:1.26-alpine AS packwiz-build
ARG PACKWIZ_REF=ef87d964f8cb
RUN go install github.com/packwiz/packwiz@${PACKWIZ_REF}

# This service exposes the Packwiz source to the Minecraft container. It is
# deliberately separate from the server so that the latter exercises the same
# Packwiz installer workflow used by a real deployment.
FROM alpine:3.22 AS packwiz-source
RUN adduser -D -u 1000 packwiz
COPY --from=packwiz-build /go/bin/packwiz /usr/local/bin/packwiz
COPY --chown=packwiz:packwiz . /pack
USER packwiz
WORKDIR /pack
EXPOSE 8080
CMD ["packwiz", "serve", "--port", "8080", "--refresh=false"]
